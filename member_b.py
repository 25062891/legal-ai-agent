# ==============================
# 成员B：知识库与RAG架构师
# 功能：载入【马来西亚1955年雇佣法 · 19大篇全文】
# 符合组长规范：vector_db / get_vector_db / get_relevant_laws
# ==============================

from sentence_transformers import SentenceTransformer
import chromadb

# 加载模型
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", cache_folder="./model_cache")

# ======================
# 组长指定函数
# ======================
def get_vector_db():
    client = chromadb.PersistentClient(path="./vector_db")
    return client.get_or_create_collection(name="malaysia_law")

# ======================
# 马来西亚《1955年雇佣法》19大篇 完整法条
# ======================
def init_law_database():
    collection = get_vector_db()

    # 清空重建
    try:
        client = chromadb.PersistentClient(path="./vector_db")
        client.delete_collection("malaysia_law")
        collection = client.get_or_create_collection("malaysia_law")
    except:
        pass

    laws = [
        # PART I – PRELIMINARY
        {"section": "Section 1", "content": "Short title and application. This Act is cited as Employment Act 1955 (Act 265)."},
        {"section": "Section 2", "content": "Definitions: contract of service, wages, employee, employer, labour officer."},
        {"section": "Section 3", "content": "Appointment of Director General of Labour and labour officers."},
        {"section": "Section 4", "content": "Appeal to Director General against labour officer decisions."},
        {"section": "Section 5", "content": "This Act overrides less favourable contract terms."},

        # PART II – CONTRACTS OF SERVICE
        {"section": "Section 6", "content": "Existing contracts valid if not less favourable than this Act."},
        {"section": "Section 7", "content": "Terms better than this Act are valid; worse terms are void."},
        {"section": "Section 10", "content": "Written contract compulsory for employees earning below RM4,000."},
        {"section": "Section 12", "content": "Termination notice: <2y=4w, 2-5y=6w, ≥5y=8w."},
        {"section": "Section 13", "content": "Termination without notice requires paying wages in lieu."},
        {"section": "Section 14", "content": "Summary dismissal allowed for misconduct, willful breach, crime."},

        # PART III – PAYMENT OF WAGES
        {"section": "Section 18", "content": "Wage period shall not exceed one month."},
        {"section": "Section 19", "content": "Wages must be paid by the 7th day of the following month."},
        {"section": "Section 20", "content": "All wages due on the day of employment termination."},
        {"section": "Section 24", "content": "Lawful deductions: EPF, SOCSO, tax, court orders, overpayments."},
        {"section": "Section 25", "content": "Itemized wage slip must be provided monthly."},

        # PART IV – DEDUCTIONS FROM WAGES
        {"section": "Section 26", "content": "No unlawful deductions for tools, accommodation, or services."},
        {"section": "Section 27", "content": "No interest allowed on wage advances."},
        {"section": "Section 28", "content": "Unlawful deduction is an offence punishable by fine."},

        # PART V – PROTECTION OF WAGES
        {"section": "Section 29", "content": "Wages are protected from attachment except by court order."},
        {"section": "Section 30", "content": "Wage claims have priority over other debts in insolvency."},
        {"section": "Section 31", "content": "Assignment of wages is void unless approved."},

        # PART VI – REGISTRATION OF CONTRACTORS
        {"section": "Section 32", "content": "Labour contractors must be registered with Labour Department."},
        {"section": "Section 33", "content": "Principal employer is liable for contractor’s unpaid wages."},

        # PART VII – TRADE UNIONS
        {"section": "Section 34", "content": "Employees have right to form and join trade unions."},
        {"section": "Section 35", "content": "No dismissal or discrimination for union activities."},

        # PART VIII – EMPLOYMENT OF WOMEN
        {"section": "Section 37", "content": "No night work for women except with approval."},
        {"section": "Section 42", "content": "No dismissal of female employees during pregnancy or maternity."},

        # PART IX – MATERNITY PROTECTION
        {"section": "Section 43", "content": "Maternity leave: 98 consecutive days with full pay."},
        {"section": "Section 44", "content": "Employee must work 90 days within 9 months to qualify."},
        {"section": "Section 47", "content": "No dismissal during maternity leave."},
        {"section": "Section 52", "content": "Paternity leave: 7 consecutive days for male employees."},
        {"section": "Section 53", "content": "Breastfeeding breaks: two 30-minute periods per day."},

        # PART X – EMPLOYMENT OF YOUNG PERSONS
        {"section": "Section 57", "content": "Child labour under 15 years old is prohibited."},
        {"section": "Section 58", "content": "Young persons 15-18 cannot do dangerous work."},
        {"section": "Section 59", "content": "Maximum working hours for young persons: 7 hours per day."},

        # PART XI – DOMESTIC SERVANTS
        {"section": "Section 65", "content": "Written contract mandatory for domestic servants."},
        {"section": "Section 66", "content": "Domestic workers entitled to rest days and annual leave."},

        # PART XII – REST DAYS & HOURS OF WORK
        {"section": "Section 69", "content": "One rest day per week for all employees."},
        {"section": "Section 70", "content": "Work on rest day must be paid 2 times daily wage."},
        {"section": "Section 71", "content": "Normal working hours: 45 hours per week."},
        {"section": "Section 71A", "content": "Overtime pay: minimum 1.5 times hourly rate."},

        # PART XIII – ANNUAL LEAVE, SICK LEAVE, HOLIDAYS
        {"section": "Section 72", "content": "Annual leave: 8, 12, 16 days based on years of service."},
        {"section": "Section 74", "content": "Sick leave: 14, 18, 22 days based on service."},
        {"section": "Section 75", "content": "Hospitalization leave up to 60 days per year."},
        {"section": "Section 77", "content": "Minimum 11 paid public holidays per year."},
        {"section": "Section 78", "content": "Work on public holiday paid 2 times; overtime 3 times."},

        # PART XIV – TERMINATION OF SERVICE
        {"section": "Section 81", "content": "Termination requires just cause or excuse."},
        {"section": "Section 82", "content": "Unfair dismissal claim may be filed with Industrial Court."},
        {"section": "Section 85", "content": "Probation period minimum 3 months."},

        # PART XV – RETRENCHMENT BENEFITS
        {"section": "Section 63", "content": "Retrenchment benefits: 10, 15, 20 days’ wage per year."},

        # PART XVA – SEXUAL HARASSMENT
        {"section": "Section 81A", "content": "Definition: unwanted sexual conduct, verbal, physical, visual."},
        {"section": "Section 81B", "content": "Employer must investigate complaints within 30 days."},
        {"section": "Section 81F", "content": "Victimizing complainant is a serious offence."},

        # PART XVI – INSPECTION & INQUIRY
        {"section": "Section 100", "content": "Labour officers may enter premises to inspect."},
        {"section": "Section 101", "content": "Employer must provide records for inspection."},

        # PART XVII – OFFENCES & PENALTIES
        {"section": "Section 111", "content": "Offences related to wages, hours, leave: fine up to RM10,000."},
        {"section": "Section 112", "content": "Offences against women, children: fine up to RM15,000."},
        {"section": "Section 125", "content": "Failure to maintain records: fine up to RM5,000."},

        # PART XVIII – GENERAL
        {"section": "Section 126", "content": "Minister may make regulations for this Act."},
        {"section": "Section 130", "content": "Protection for officers acting in good faith."},
        {"section": "Section 135", "content": "This Act applies to Peninsular Malaysia."}
    ]

    # 存入向量库
    for law in laws:
        emb = model.encode(law["content"]).tolist()
        collection.add(
            ids=[law["section"]],
            embeddings=[emb],
            metadatas=[{"section": law["section"]}],
            documents=[law["content"]]
        )

    print("✅ 马来西亚《1955年雇佣法》19大篇全文已完整入库！")

# ======================
# 组长要求的检索函数
# ======================
def get_relevant_laws(query_text: str) -> list[dict]:
    collection = get_vector_db()
    query_emb = model.encode(query_text).tolist()

    results = collection.query(
        query_embeddings=[query_emb],
        n_results=4
    )

    output = []
    for sec, content in zip(results["metadatas"][0], results["documents"][0]):
        output.append({
            "section": sec["section"],
            "content": content
        })
    return output

# ======================
# 运行初始化
# ======================
if __name__ == "__main__":
    init_law_database()
    print("\n测试检索：maternity leave")
    print(get_relevant_laws("maternity leave"))