def extract_time_scope(claim, judge):
    prompt = f"""
    Extract the TEMPORAL SCOPE (T^q) from the following claim.
    Claim: "{claim}"

    Rules:
    - Extract explicit years, ages, or narrative periods.
    - Return ONLY the extracted terms.
    - If none exist, return "General".
    """
    try:
        return judge.invoke(prompt).content.strip()
    except:
        return "General"
