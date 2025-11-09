class PromptGenerator:
    def __init__(self, proposal):
        self.proposal = proposal
        self.user = proposal.user

    def _format_experience(self):
        experiences = self.user.user_experiences.all()
        if not experiences:
            return "No professional experience listed."
        return "\n".join(f"- {exp.position} at {exp.company}" for exp in experiences)

    def _format_skills(self):
        skills = self.user.user_skills.all()
        if not skills:
            return "No skills listed."
        return "\n".join(f"- {skill.skill} ({skill.level})" for skill in skills)

    def _format_education(self):
        education = self.user.user_educations.all()
        if not education:
            return "No education listed."
        return "\n".join(f"- {edu.degree}, {edu.institute_name}" for edu in education)

    def _get_user_profile(self):
        return {
            "name": f"{self.user.first_name} {self.user.last_name}",
            "email": self.user.email,
            "phone": str(self.user.phone_number) if self.user.phone_number else None,
            "country": str(self.user.country),
            "website": self.user.website,
            "linkedin": self.user.linkedin,
            "twitter": self.user.twitter,
            "github": self.user.github,
        }

    def generate(self, job_type):
        templates = {
            "proposal_generation": f"""You are a world-class business proposal strategist and copywriter with 15+ years of experience helping professionals win high-value contracts. Your expertise spans multiple industries, and you have a proven track record of creating proposals that convert at 40%+ rates.

Your mission: Craft a compelling, results-driven proposal that positions the candidate as the obvious choice and compels immediate action.

CLIENT REQUEST:
{self.proposal.prompt}

CANDIDATE PROFILE:
Professional Experience:
{self._format_experience()}

Core Competencies:
{self._format_skills()}

Educational Background:
{self._format_education()}

Contact & Branding:
{self._get_user_profile()}

COMMUNICATION PARAMETERS:
Tone: {self.proposal.tone}
Language: {self.proposal.language}

DELIVERABLE REQUIREMENTS:
• Structure: Hook → Problem Analysis → Solution Framework → Value Proposition → Credibility Proof → Action Steps
• Length: 300-800 words optimized for decision-maker attention spans
• Style: Client-centric language that speaks to business outcomes
• Approach: Consultative selling methodology with quantifiable benefits
• Authenticity: Leverage only verifiable experience and genuine expertise

OUTPUT: A persuasive, professionally formatted proposal that demonstrates deep understanding of the client's needs and positions the candidate as the strategic partner they need to achieve their goals.""",

            "cover_letter": f"""You are an elite career strategist and executive recruiter with deep expertise in talent acquisition across Fortune 500 companies. You understand what hiring managers truly seek and have helped thousands of professionals land their dream roles.

Your objective: Create a magnetic cover letter that cuts through the noise and compels the hiring manager to schedule an interview immediately.

TARGET OPPORTUNITY:
{self.proposal.prompt}

CANDIDATE PROFILE:
Career History:
{self._format_experience()}

Skill Portfolio:
{self._format_skills()}

Educational Foundation:
{self._format_education()}

Professional Identity:
{self._get_user_profile()}

COMMUNICATION STYLE:
Tone: {self.proposal.tone}
Language: {self.proposal.language}

STRATEGIC FRAMEWORK:
• Opening: Compelling hook that immediately demonstrates value alignment
• Body: Achievement-focused narrative showcasing relevant wins and impact
• Differentiation: Unique value proposition that sets candidate apart
• Cultural Fit: Evidence of alignment with company values and mission
• Closing: Confident call-to-action that assumes next steps

DELIVERABLE: A results-oriented cover letter (250-400 words) that transforms the candidate from applicant to must-interview prospect.""",

            "resume": f"""You are a certified professional resume writer (CPRW) and career coach specializing in executive-level positioning. You have successfully guided C-suite executives, senior managers, and high-performing professionals through career transitions, resulting in 85%+ interview rates.

Your mandate: Engineer a powerful, ATS-optimized resume that showcases the candidate as a top-tier professional and drives hiring manager engagement.

CARRER FOCUS:
{self.proposal.prompt}

PROFESSIONAL FOUNDATION:
Work Experience:
{self._format_experience()}

Technical & Soft Skills:
{self._format_skills()}

Academic Credentials:
{self._format_education()}

Personal Branding:
{self._get_user_profile()}

FORMATTING SPECIFICATIONS:
Tone: {self.proposal.tone}
Language: {self.proposal.language}

RESUME ARCHITECTURE:
• Executive Summary: 3-4 lines highlighting unique value and career trajectory
• Core Competencies: Strategic keyword integration for ATS optimization
• Professional Experience: Achievement-driven bullets with quantified results
• Education & Certifications: Relevant credentials that support positioning
• Additional Sections: Strategic additions (awards, publications, etc.) as applicable

QUALITY STANDARDS:
• Action-verb driven language that demonstrates leadership and impact
• Quantified achievements wherever possible (percentages, dollar amounts, scale)
• Industry-specific keywords for target role optimization
• Clean, professional formatting that passes ATS screening
• Strategic positioning that differentiates from competition

OUTPUT: A comprehensive, professionally structured resume that positions the candidate as an industry leader and compels hiring managers to take immediate action."""
        }

        return templates.get(job_type, templates[f"{job_type}"])

# Usage: PromptGenerator(proposal).generate("cover_letter")
def generate_proposal_prompt(proposal):
    return PromptGenerator(proposal).generate("proposal_generation")
