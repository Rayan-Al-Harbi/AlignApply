from langchain_text_splitters import RecursiveCharacterTextSplitter



sample_cv = """
Name: Sarah Chen

Summary:
Experienced software engineer with 4 years of backend development, specializing in Python and cloud infrastructure.

Skills:
Python, Django, REST APIs, PostgreSQL, Docker, AWS, Git, Linux

Experience:
- Software Engineer at TechCorp (2021 - Present)
  Built and maintained microservices using Python and Django. Deployed services on AWS using Docker.

- Junior Developer at StartupXYZ (2020 - 2021)
  Developed internal REST APIs and managed PostgreSQL databases.

Education:
- B.Sc. Computer Science, University of Cityville, 2020
"""

SECTION_HEADERS = {
    # Identity / intro
    "name", "contact", "contact information", "personal information", "personal details",
    "profile", "about", "about me", "objective", "career objective", "professional objective",
    "summary", "professional summary", "executive summary", "career summary",

    # Skills
    "skills", "technical skills", "core skills", "key skills", "hard skills", "soft skills",
    "competencies", "core competencies", "areas of expertise", "expertise",
    "tools", "tools & technologies", "technologies", "tech stack",
    "programming languages", "frameworks", "libraries",

    # Experience
    "experience", "work experience", "professional experience", "employment history",
    "career history", "work history", "relevant experience", "internships",
    "internship experience", "volunteer experience", "volunteering",

    # Education
    "education", "academic background", "academic history", "qualifications",
    "educational background", "degrees", "training", "academic qualifications",

    # Projects
    "projects", "personal projects", "academic projects", "key projects",
    "notable projects", "open source", "open-source contributions", "portfolio",

    # Certifications & awards
    "certifications", "certificates", "licenses", "accreditations",
    "awards", "honors", "achievements", "accomplishments", "recognition",

    # Languages
    "languages", "language skills", "spoken languages",

    # Publications & research
    "publications", "research", "research experience", "papers", "patents",

    # Extras
    "interests", "hobbies", "activities", "extracurricular activities",
    "references", "referees", "additional information",
}

def chunk_cv(cv_text: str) -> list[str]:
    lines = cv_text.splitlines()
    chunks = []
    current_section_lines = []

    for line in lines:
        normalized = line.strip().lower().lstrip("#-= ").rstrip("#-= :")
        is_header = normalized in SECTION_HEADERS
        if is_header and current_section_lines:
            chunk = "\n".join(current_section_lines).strip()
            if chunk:
                chunks.append(chunk)
            current_section_lines = [line]
        else:
            current_section_lines.append(line)

    # flush last section
    if current_section_lines:
        chunk = "\n".join(current_section_lines).strip()
        if chunk:
            chunks.append(chunk)

    return chunks

if __name__ == "__main__":
    results = chunk_cv(sample_cv)
    for chunk in results:
        print(chunk)
        print("\n HERE\n")
