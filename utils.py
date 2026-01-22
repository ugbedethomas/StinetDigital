from .models import StudentSkill, JobPosting


def calculate_job_match(student, job):
    """
    Calculate match percentage between student and job
    Returns: Float percentage (0-100)
    """
    # Get verified student skills
    student_skills = set(
        StudentSkill.objects.filter(
            student=student,
            verified=True
        ).values_list('skill__name', flat=True)
    )

    # Get required job skills
    required_skills = set(
        job.skills_required.values_list('name', flat=True)
    )

    if not required_skills:
        return 0.0

    # Calculate basic skill match
    matched_skills = student_skills.intersection(required_skills)
    skill_match = (len(matched_skills) / len(required_skills)) * 60  # 60% weight

    # Experience level match (simplified)
    experience_bonus = 0
    if student.profile.experience_level == job.experience_level:
        experience_bonus = 20  # 20% bonus

    # Course completion bonus
    course_bonus = 0
    # Add logic here based on completed courses related to job skills

    total_match = min(100, skill_match + experience_bonus + course_bonus)

    return round(total_match, 1)