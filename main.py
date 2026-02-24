from orchestrator import ScrappyOrchestrator

scrappyOrchestrator = ScrappyOrchestrator()

result = scrappyOrchestrator.investigate(question="Why are the sales low in last couple of weeks?")

#Test the output of intent agent
print(result['question'])
print(result['question_type'])
print(result['metrics_mentioned'])
print(result['dimensions'])

for sql in result['generated_queries']:
    print(sql['query'])

print("Done") 