from evaluate_native_checkpoint import DEFAULT_PROMPTS,evaluate_text
def main():
 bad=[
  "I can make a plan for you.",
  "I don't know what you mean by shifts or off days.",
  "I can suggest ways to manage your finances.",
  "Let me know if you'd like to refine this further.",
  "Give me a memory receipt and I will proceed with the action.",
  "If you have specific questions, feel free to ask.",
 ]
 for prompt,text in zip(DEFAULT_PROMPTS,bad):
  result=evaluate_text(prompt,text)
  assert not result["semantic_pass"] and result["rubric_failures"],(prompt,result)
 print("PASS canonical rubrics reject fluent but non-responsive answers")
if __name__=="__main__":main()
