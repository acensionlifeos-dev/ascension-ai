from train_qwen_ascension_lora import SYSTEM_PROMPTS

def main():
    ap=SYSTEM_PROMPTS["ap"].casefold(); life=SYSTEM_PROMPTS["lifeos"].casefold()
    assert "not saved" in ap and "preparation is not execution" in ap
    assert "timeout" in ap and "unknown" in ap and "provider receipt" in ap
    assert "connection does not prove" in life and "upload does not prove" in life
    assert "without repeating" in SYSTEM_PROMPTS["nexus_family"].casefold()
    assert "instead of restating" in SYSTEM_PROMPTS["creation"].casefold()
    print("PASS explicit state-machine system prompt contract")

if __name__=="__main__": main()
