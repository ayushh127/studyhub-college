def update_community_material_moderation(material):
    """
    Recalculates the moderation score for a community material based on reports,
    likes, ratings, and views. If the score or conditions reach a certain threshold,
    the material is automatically set to 'under_review'.
    """
    views = max(material.views_count, 1)
    report_rate = material.reports_count / views
    like_rate = material.likes_count / views
    rating_score = material.average_rating / 5.0
    
    risk_score = (report_rate * 100) + (material.reports_count * 3) - (like_rate * 40) - (rating_score * 20)
    
    material.moderation_score = risk_score
    
    # Escalation Rules
    if (material.reports_count >= 5) or \
       (material.reports_count >= 3 and risk_score >= 25) or \
       (report_rate >= 0.25 and material.views_count >= 10) or \
       (material.average_rating <= 2.0 and material.ratings_count >= 5 and material.reports_count >= 2):
        material.status = 'under_review'

    return risk_score
