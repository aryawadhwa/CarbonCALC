"""
Biosafety and Sustainability Recommendation Engine
Generates personalized recommendations based on carbon footprint analysis
"""
from typing import List, Dict, Any
from database.models import UserType


class RecommendationEngine:
    """
    Generates personalized sustainability recommendations
    """
    
    RECOMMENDATIONS_LIBRARY = {
        "energy": [
            {
                "title": "Industrial Energy Efficiency Audit",
                "description": "Conduct a comprehensive audit of industrial machinery. Optimizing motors and thermal systems can reduce emissions by 20-30%.",
                "impact_rating": 5,
                "difficulty": "medium",
                "estimated_reduction": 5000,
                "cost_estimate": "medium"
            },
            {
                "title": "Renewable Energy Transition",
                "description": "Switch facility power to renewable sources (solar/wind). Critical for reducing Scope 2 emissions in manufacturing.",
                "impact_rating": 5,
                "difficulty": "hard",
                "estimated_reduction": 10000,
                "cost_estimate": "high"
            },
            {
                "title": "Heat Recovery Systems",
                "description": "Install waste heat recovery units on exhaust stacks. Reusing thermal energy improves biosafety by reducing thermal pollution.",
                "impact_rating": 4,
                "difficulty": "medium",
                "estimated_reduction": 3000,
                "cost_estimate": "medium"
            }
        ],
        "transportation": [
            {
                "title": "Green Logistics Optimization",
                "description": "Optimize supply chain routes to minimize fuel consumption. Use fleet management software for real-time tracking.",
                "impact_rating": 4,
                "difficulty": "medium",
                "estimated_reduction": 4000,
                "cost_estimate": "medium"
            },
            {
                "title": "Electric Fleet Conversion",
                "description": "Transition logistics fleet to electric vehicles. Reduces particulate matter and improves local air quality (biosafety).",
                "impact_rating": 5,
                "difficulty": "hard",
                "estimated_reduction": 8000,
                "cost_estimate": "high"
            }
        ],
        "waste": [
            {
                "title": "Hazardous Waste Neutralization",
                "description": "Implement on-site neutralization for chemical/biological waste. Prevents environmental contamination and ensures biosafety compliance.",
                "impact_rating": 5,
                "difficulty": "hard",
                "estimated_reduction": 2000,
                "cost_estimate": "high"
            },
            {
                "title": "Circular Economy Integration",
                "description": "Repurpose industrial byproducts as raw materials. Reduces landfill usage and raw material extraction impact.",
                "impact_rating": 4,
                "difficulty": "medium",
                "estimated_reduction": 5000,
                "cost_estimate": "medium"
            },
            {
                "title": "Zero-Liquid Discharge (ZLD)",
                "description": "Implement ZLD systems to treat wastewater. Recovers water for reuse and eliminates liquid waste discharge.",
                "impact_rating": 5,
                "difficulty": "hard",
                "estimated_reduction": 3000,
                "cost_estimate": "high"
            }
        ],
        "food": [
            {
                "title": "Sustainable Canteen Sourcing",
                "description": "Source cafeteria food from local, sustainable producers. Reduces food miles and supports local biosafety standards.",
                "impact_rating": 3,
                "difficulty": "easy",
                "estimated_reduction": 1000,
                "cost_estimate": "low"
            }
        ],
        "water": [
            {
                "title": "Industrial Water Recycling",
                "description": "Treat and recycle process water. Reduces demand on local aquifers and minimizes effluent discharge.",
                "impact_rating": 4,
                "difficulty": "medium",
                "estimated_reduction": 2000,
                "cost_estimate": "medium"
            },
            {
                "title": "Effluent Treatment Plant (ETP) Upgrade",
                "description": "Upgrade ETP with advanced filtration. Ensures discharged water meets strict biosafety parameters.",
                "impact_rating": 5,
                "difficulty": "hard",
                "estimated_reduction": 1500,
                "cost_estimate": "high"
            }
        ],
        "corporate": [
            {
                "title": "ISO 14001 Certification",
                "description": "Implement Environmental Management Systems. Standardizes biosafety and sustainability protocols across operations.",
                "impact_rating": 5,
                "difficulty": "hard",
                "estimated_reduction": 15000,
                "cost_estimate": "high"
            },
            {
                "title": "Biosafety Compliance Audit",
                "description": "Regular audits for biological and chemical safety. Identifies risks and ensures regulatory compliance.",
                "impact_rating": 5,
                "difficulty": "medium",
                "estimated_reduction": 5000,
                "cost_estimate": "medium"
            },
            {
                "title": "Supply Chain Decarbonization",
                "description": "Engage suppliers in carbon reduction. Scope 3 emissions often constitute the largest share of corporate footprint.",
                "impact_rating": 4,
                "difficulty": "hard",
                "estimated_reduction": 20000,
                "cost_estimate": "medium"
            }
        ]
    }
    
    @staticmethod
    def generate_recommendations(
        footprint_breakdown: Dict[str, float],
        user_type: UserType,
        top_n: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate personalized biosafety and mitigation recommendations
        """
        recommendations = []
        total_footprint = footprint_breakdown.get("total", 0)
        
        # Sort categories by emissions (highest first)
        categories = ["energy", "transportation", "waste", "food", "water", "corporate"]
        sorted_categories = sorted(
            categories,
            key=lambda x: footprint_breakdown.get(x, 0),
            reverse=True
        )
        
        # Get top 3 categories with highest emissions
        top_categories = sorted_categories[:3]
        
        # Generate recommendations for each top category
        for category in top_categories:
            if category in RecommendationEngine.RECOMMENDATIONS_LIBRARY:
                category_recommendations = RecommendationEngine.RECOMMENDATIONS_LIBRARY[category]
                
                # Select top 2 recommendations per category
                for rec in category_recommendations[:2]:
                    # Adjust reduction estimate for user type
                    rec_copy = rec.copy()
                    rec_copy["category"] = category
                    
                    if user_type == UserType.CORPORATION:
                        rec_copy["estimated_reduction"] *= 10
                    elif user_type == UserType.INSTITUTION:
                        rec_copy["estimated_reduction"] *= 5
                        
                    recommendations.append(rec_copy)
        
        # Add corporate-specific recommendations for all non-individual users
        if user_type in [UserType.CORPORATION, UserType.INSTITUTION]:
            for rec in RecommendationEngine.RECOMMENDATIONS_LIBRARY["corporate"][:3]:
                rec_copy = rec.copy()
                rec_copy["category"] = "corporate"
                if user_type == UserType.CORPORATION:
                     rec_copy["estimated_reduction"] *= 2
                recommendations.append(rec_copy)
        
        # Sort by impact rating and estimated reduction
        recommendations.sort(
            key=lambda x: (x["impact_rating"], x["estimated_reduction"]),
            reverse=True
        )
        
        # Assign priority
        for i, rec in enumerate(recommendations[:top_n]):
            rec["priority"] = top_n - i
        
        # Add contextual feedback
        for rec in recommendations[:top_n]:
            if "category" not in rec:
                rec["category"] = "general"
            rec["context"] = RecommendationEngine._get_contextual_feedback(
                rec["category"],
                footprint_breakdown
            )
        
        return recommendations[:top_n]
    
    @staticmethod
    def _get_contextual_feedback(category: str, footprint_breakdown: Dict[str, float]) -> str:
        """Generate contextual biosafety and mitigation feedback"""
        category_emissions = footprint_breakdown.get(category, 0)
        total = footprint_breakdown.get("total", 1)
        percentage = (category_emissions / total * 100) if total > 0 else 0
        
        feedbacks = {
            "energy": f"Energy use constitutes {percentage:.1f}% of emissions. "
                     f"Optimizing thermal systems and transitioning to renewables is critical for biosafety and carbon reduction.",
            "transportation": f"Logistics account for {percentage:.1f}% of impact. "
                            f"Electrifying fleets reduces particulate matter, directly improving local biosafety.",
            "waste": f"Waste generation is {percentage:.1f}% of your footprint. "
                    f"Proper neutralization of hazardous waste is a key biosafety requirement.",
            "food": f"Food sourcing contributes {percentage:.1f}%. "
                   f"Sustainable sourcing ensures biological safety and reduces supply chain emissions.",
            "water": f"Water usage is {percentage:.1f}%. "
                    f"Treating effluent prevents biological contamination of local water bodies.",
            "corporate": f"Operational protocols contribute significantly. "
                        f"Standardizing biosafety management systems (ISO 14001) is recommended.",
            "general": "Mitigation strategies should prioritize high-impact areas to ensure maximum biosafety and environmental protection."
        }
        
        return feedbacks.get(category, feedbacks["general"])

