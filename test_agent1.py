from app.agents.query_refiner import refine_query, extract_symptoms_structured

print("=" * 60)
print("TESTING AGENT-1: QUERY REFINEMENT")
print("=" * 60)

# Test cases: casual input → should become medical terms
test_queries = [
    "my head hurts",
    "not feeling well",
    "stomach pain and throwing up",
    "have fever since 2 days",
    "headache and fever, started yesterday, pretty bad"
]

print("\n[TEST 1] Basic Query Refinement")
print("-" * 60)
for query in test_queries:
    print(f"\nOriginal: '{query}'")
    result = refine_query(query)
    print(f"Refined:  '{result['refined_query']}'")
    print(f"Needs clarification: {result['needs_clarification']}")

print("\n" + "=" * 60)
print("[TEST 2] Structured Extraction")
print("-" * 60)

test_query = "severe headache since 2 days with fever"
print(f"\nInput: '{test_query}'")
structured = extract_symptoms_structured(test_query)
print(f"\nExtracted structure:")
print(f"  Symptoms: {structured['symptoms']}")
print(f"  Duration: {structured['duration']}")
print(f"  Severity: {structured['severity']}")
print(f"  Full refined: {structured['refined_query']}")

print("\n" + "=" * 60)
print("AGENT-1 TESTS COMPLETE")
print("=" * 60)