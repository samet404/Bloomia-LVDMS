from sentence_transformers import SentenceTransformer

# Load the model
model = SentenceTransformer("Alibaba-NLP/gte-Qwen2-7B-instruct")

# Each query must come with a one-sentence instruction that describes the task
task = 'Given a question, retrieve Wikipedia passages that answer the question'
prompt = f"Instruct: {task}\nQuery: "
queries = [
    "최초의 원자력 발전소는 무엇인가?",
    "Who invented Hangul?"
]
passages = [
    "현재 사용되는 핵분열 방식을 이용한 전력생산은 1948년 9월 미국 테네시주 오크리지에 설치된 X-10 흑연원자로에서 전구의 불을 밝히는 데 사용되면서 시작되었다. 그리고 1954년 6월에 구소련의 오브닌스크에 건설된 흑연감속 비등경수 압력관형 원자로를 사용한 오브닌스크 원자력 발전소가 시험적으로 전력생산을 시작하였고, 최초의 상업용 원자력 엉더이로를 사용한 영국 셀라필드 원자력 단지에 위치한 콜더 홀(Calder Hall) 원자력 발전소로, 1956년 10월 17일 상업 운전을 시작하였다.",
    "Hangul was personally created and promulgated by the fourth king of the Joseon dynasty, Sejong the Great.[1][2] Sejong's scholarly institute, the Hall of Worthies, is often credited with the work, and at least one of its scholars was heavily involved in its creation, but it appears to have also been a personal project of Sejong."
]

# Encode the queries and passages. We only use the prompt for the queries
query_embeddings = model.encode(queries, prompt=prompt)
passage_embeddings = model.encode(passages)

# Compute the (cosine) similarity scores
scores = model.similarity(query_embeddings, passage_embeddings) * 100
print(scores.tolist())
# [[73.72908782958984, 30.122787475585938], [29.15508460998535, 79.25375366210938]]
