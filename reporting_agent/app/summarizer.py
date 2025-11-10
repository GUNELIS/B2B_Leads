"""Hybrid summarizer with instruction-tuned model, anti-repetition, and cleanup."""
import os
from typing import Dict, Optional, List
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline, AutoModelForCausalLM

_cache = {"pipe": None, "mode": None}  # mode: "seq2seq" | "causal"

def _load_pipe():
    if _cache["pipe"] is not None:
        return _cache["pipe"], _cache["mode"]

    # Prefer an instruction-tuned seq2seq model (cleaner, less echo).
    model_name = os.getenv("LLM_MODEL_NAME", "google/flan-t5-small")
    try:
        tok = AutoTokenizer.from_pretrained(model_name)
        mdl = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        _cache["pipe"] = pipeline("text2text-generation", model=mdl, tokenizer=tok, device=-1)
        _cache["mode"] = "seq2seq"
        return _cache["pipe"], _cache["mode"]
    except Exception:
        # Fallback to tiny causal; enforce repetition controls.
        model_name = os.getenv("LLM_MODEL_NAME", "sshleifer/tiny-gpt2")
        tok = AutoTokenizer.from_pretrained(model_name)
        mdl = AutoModelForCausalLM.from_pretrained(model_name)
        _cache["pipe"] = pipeline("text-generation", model=mdl, tokenizer=tok, device=-1)
        _cache["mode"] = "causal"
        return _cache["pipe"], _cache["mode"]

def _join_top(items: Optional[List[dict]], key: str, k: int = 3) -> str:
    if not items:
        return "N/A"
    names = [d.get(key) for d in items if d.get(key)]
    return ", ".join(names[:k]) if names else "N/A"

def _clean_sentences(text: str, max_sents: int = 6) -> str:
    # Normalize whitespace and split crudely on sentence endings.
    import re
    text = re.sub(r"\s+", " ", text).strip()
    parts = re.split(r"(?<=[.!?])\s+", text)
    # Deduplicate consecutive repeats.
    cleaned = []
    seen = set()
    for p in parts:
        if not p:
            continue
        sig = p.lower()
        if cleaned and sig == cleaned[-1].lower():
            continue
        cleaned.append(p)
    # Cap length.
    return " ".join(cleaned[:max_sents]).strip()

def summarize(stats: Dict) -> str:
    if not stats or stats.get("count", 0) == 0:
        return "No match data available to summarize."

    count = stats.get("count", 0)
    s = stats.get("score", {}) or {}
    mean, p90 = s.get("mean"), s.get("p90")

    # Handle misspelled key from upstream: top_industrys
    inds_key = "top_industries" if "top_industries" in stats else "top_industrys"
    inds_str = _join_top(stats.get(inds_key), "industry")
    regs_str = _join_top(stats.get("top_regions"), "region")

    # Deterministic baseline, always returned if model fails.
    base = (
        f"The dataset includes {count} lead–company matches. "
        f"Average compatibility score is {mean if mean is not None else 'N/A'}, "
        f"with the top 10% above {p90 if p90 is not None else 'N/A'}. "
        f"Leading industries: {inds_str}. Top regions: {regs_str}."
    )

    pipe, mode = _load_pipe()

    try:
        if mode == "seq2seq":
            prompt = (
                "You write concise executive analytics summaries.\n"
                f"Total matches: {count}\n"
                f"Average score: {mean}\n"
                f"90th percentile: {p90}\n"
                f"Top industries: {inds_str}\n"
                f"Top regions: {regs_str}\n"
                "Write 4–6 sentences: key trends, plausible drivers, and one implication."
            )
            out = pipe(
                prompt,
                max_new_tokens=160,
                do_sample=False,
                repetition_penalty=1.05,
            )[0]["generated_text"]
        else:
            # Causal fallback: prepend context, then ask for continuation.
            prompt = (
                base + " Provide 3 additional concise business insight sentences."
            )
            out = pipe(
                prompt,
                max_new_tokens=120,
                do_sample=True,
                temperature=0.5,
                top_p=0.9,
                no_repeat_ngram_size=4,
                repetition_penalty=1.2,
                eos_token_id=pipe.tokenizer.eos_token_id,
                pad_token_id=getattr(pipe.tokenizer, "pad_token_id", pipe.tokenizer.eos_token_id),
            )[0]["generated_text"]
            # Remove the prompt prefix if present.
            if out.startswith(prompt):
                out = out[len(prompt):].strip()

        enriched = _clean_sentences(out)
        # If model yielded nothing useful, return baseline.
        return base if not enriched else f"{base} {enriched}"
    except Exception:
        return base
