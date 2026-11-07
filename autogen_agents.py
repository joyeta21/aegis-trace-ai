def generate_dpdp_notice(target_entity, user_name="Joyeta Pal", user_phone="+91-9876543210"):
    notice = f"""
    FORMAL LEGAL NOTICE FOR DATA ERASURE & CONSENT REVOCATION
    Under Section 12 of the Digital Personal Data Protection (DPDP) Act, India

    To,
    The Data Protection Officer (DPO) / Grievance Redressal Officer
    {target_entity}

    Subject: Demand for Immediate Erasure of Personal Data and Revocation of Consent

    Dear Sir/Madam,

    I am writing to you as a Data Principal to formally demand the complete, permanent erasure of my personal data (Phone: {user_phone}, Name: {user_name}) stored, processed, or shared by {target_entity} and its affiliates.
    
    In accordance with Section 12 of the DPDP Act 2023, I hereby withdraw my consent for data processing. Please confirm complete erasure within 7 business days.

    Sincerely,
    {user_name}
    Data Principal
    """
    return notice