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
                "title": "Switch to Renewable Energy",
                "description": "Consider switching to a renewable energy provider or installing solar panels. This can reduce your electricity emissions by up to 90%.",
                "impact_rating": 5,
                "difficulty": "medium",
                "estimated_reduction": 500,  # kg CO2 per year
                "cost_estimate": "medium"
            },
            {
                "title": "Use Energy-Efficient Appliances",
                "description": "Replace old appliances with Energy Star rated ones. Upgrade to LED lighting throughout your home/office.",
                "impact_rating": 4,
                "difficulty": "easy",
                "estimated_reduction": 300,
                "cost_estimate": "medium"
            },
            {
                "title": "Optimize Heating and Cooling",
                "description": "Use programmable thermostats, improve insulation, and seal air leaks. Lower heating by 2°C and raise cooling by 2°C.",
                "impact_rating": 3,
                "difficulty": "easy",
                "estimated_reduction": 200,
                "cost_estimate": "low"
            },
            {
                "title": "Unplug Electronics When Not in Use",
                "description": "Use power strips and unplug devices when not in use to eliminate phantom energy consumption.",
                "impact_rating": 2,
                "difficulty": "easy",
                "estimated_reduction": 100,
                "cost_estimate": "free"
            }
        ],
        "transportation": [
            {
                "title": "Use Public Transportation",
                "description": "Switch to public transport, cycling, or walking for daily commutes. Consider carpooling or ride-sharing.",
                "impact_rating": 5,
                "difficulty": "easy",
                "estimated_reduction": 1000,
                "cost_estimate": "low"
            },
            {
                "title": "Switch to Electric Vehicle",
                "description": "If you need a car, consider an electric vehicle. Even with grid electricity, EVs have lower emissions.",
                "impact_rating": 5,
                "difficulty": "hard",
                "estimated_reduction": 2000,
                "cost_estimate": "high"
            },
            {
                "title": "Reduce Air Travel",
                "description": "Opt for video conferencing instead of business flights. Combine trips when possible, choose direct flights.",
                "impact_rating": 4,
                "difficulty": "medium",
                "estimated_reduction": 1500,
                "cost_estimate": "free"
            },
            {
                "title": "Maintain Vehicle Efficiency",
                "description": "Keep tires properly inflated, maintain regular servicing, and practice eco-driving techniques.",
                "impact_rating": 2,
                "difficulty": "easy",
                "estimated_reduction": 150,
                "cost_estimate": "low"
            }
        ],
        "waste": [
            {
                "title": "Increase Recycling Rate",
                "description": "Improve waste segregation, compost organic waste, and ensure proper recycling of paper, plastic, and metal.",
                "impact_rating": 4,
                "difficulty": "easy",
                "estimated_reduction": 400,
                "cost_estimate": "free"
            },
            {
                "title": "Reduce Single-Use Plastics",
                "description": "Switch to reusable bags, bottles, and containers. Avoid single-use plastics and packaging.",
                "impact_rating": 3,
                "difficulty": "easy",
                "estimated_reduction": 200,
                "cost_estimate": "low"
            },
            {
                "title": "Compost Organic Waste",
                "description": "Start composting food scraps and yard waste. This reduces landfill methane emissions significantly.",
                "impact_rating": 3,
                "difficulty": "medium",
                "estimated_reduction": 300,
                "cost_estimate": "low"
            },
            {
                "title": "Implement Zero-Waste Practices",
                "description": "Adopt zero-waste principles: refuse, reduce, reuse, recycle, rot. Focus on waste prevention.",
                "impact_rating": 4,
                "difficulty": "medium",
                "estimated_reduction": 500,
                "cost_estimate": "low"
            }
        ],
        "food": [
            {
                "title": "Reduce Meat Consumption",
                "description": "Adopt a more plant-based diet. Try 'Meatless Mondays' or reduce meat portions. Plant-based proteins have much lower emissions.",
                "impact_rating": 5,
                "difficulty": "medium",
                "estimated_reduction": 600,
                "cost_estimate": "low"
            },
            {
                "title": "Buy Local and Seasonal Produce",
                "description": "Reduce food miles by purchasing local, seasonal produce. Support local farmers and reduce transportation emissions.",
                "impact_rating": 3,
                "difficulty": "easy",
                "estimated_reduction": 200,
                "cost_estimate": "medium"
            },
            {
                "title": "Reduce Food Waste",
                "description": "Plan meals, use leftovers creatively, and store food properly. Food waste in landfills produces methane.",
                "impact_rating": 4,
                "difficulty": "easy",
                "estimated_reduction": 350,
                "cost_estimate": "free"
            },
            {
                "title": "Choose Sustainable Seafood",
                "description": "If consuming seafood, choose sustainably sourced options. Consider the environmental impact of your choices.",
                "impact_rating": 2,
                "difficulty": "easy",
                "estimated_reduction": 100,
                "cost_estimate": "medium"
            }
        ],
        "water": [
            {
                "title": "Install Water-Efficient Fixtures",
                "description": "Install low-flow showerheads, faucets, and toilets. This reduces both water usage and energy for heating.",
                "impact_rating": 3,
                "difficulty": "easy",
                "estimated_reduction": 150,
                "cost_estimate": "low"
            },
            {
                "title": "Fix Leaks Promptly",
                "description": "Regularly check for and fix leaks. A single leaky faucet can waste significant amounts of water.",
                "impact_rating": 2,
                "difficulty": "easy",
                "estimated_reduction": 50,
                "cost_estimate": "low"
            },
            {
                "title": "Use Rainwater Harvesting",
                "description": "Collect and use rainwater for irrigation and non-potable uses. Reduces demand on municipal water.",
                "impact_rating": 2,
                "difficulty": "medium",
                "estimated_reduction": 100,
                "cost_estimate": "medium"
            }
        ],
        "corporate": [
            {
                "title": "Implement Remote Work Policy",
                "description": "Allow employees to work from home several days per week. This significantly reduces commute emissions.",
                "impact_rating": 5,
                "difficulty": "medium",
                "estimated_reduction": 5000,  # for corporation
                "cost_estimate": "low"
            },
            {
                "title": "Green Building Certification",
                "description": "Pursue LEED or similar green building certifications. Optimize building energy efficiency and materials.",
                "impact_rating": 5,
                "difficulty": "hard",
                "estimated_reduction": 10000,
                "cost_estimate": "high"
            },
            {
                "title": "Employee Sustainability Program",
                "description": "Educate employees on sustainability practices. Offer incentives for green commuting and sustainable behaviors.",
                "impact_rating": 4,
                "difficulty": "medium",
                "estimated_reduction": 2000,
                "cost_estimate": "low"
            },
            {
                "title": "Optimize Supply Chain",
                "description": "Work with suppliers to reduce transportation distances, use sustainable materials, and minimize packaging.",
                "impact_rating": 4,
                "difficulty": "hard",
                "estimated_reduction": 8000,
                "cost_estimate": "medium"
            },
            {
                "title": "Carbon Offsetting Program",
                "description": "Implement a corporate carbon offset program for unavoidable emissions. Invest in verified carbon reduction projects.",
                "impact_rating": 3,
                "difficulty": "medium",
                "estimated_reduction": 0,  # offsets, not reduces
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
        Generate personalized recommendations based on carbon footprint breakdown
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
                
                # Adjust for corporate/institutional users
                if user_type in [UserType.CORPORATION, UserType.INSTITUTION] and category != "corporate":
                    # Still include, but with adjusted messaging
                    pass
                
                # Select top 2 recommendations per category
                for rec in category_recommendations[:2]:
                    # Adjust reduction estimate for user type
                    if user_type == UserType.CORPORATION and "corporate" not in category:
                        # Scale up for corporations
                        rec_copy = rec.copy()
                        rec_copy["category"] = category
                        rec_copy["estimated_reduction"] = rec["estimated_reduction"] * 10
                        recommendations.append(rec_copy)
                    elif user_type == UserType.INSTITUTION:
                        rec_copy = rec.copy()
                        rec_copy["category"] = category
                        rec_copy["estimated_reduction"] = rec["estimated_reduction"] * 5
                        recommendations.append(rec_copy)
                    else:
                        rec_copy = rec.copy()
                        rec_copy["category"] = category
                        recommendations.append(rec_copy)
        
        # Add corporate-specific recommendations if applicable
        if user_type in [UserType.CORPORATION, UserType.INSTITUTION]:
            for rec in RecommendationEngine.RECOMMENDATIONS_LIBRARY["corporate"][:3]:
                rec_copy = rec.copy()
                rec_copy["category"] = "corporate"
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
        """Generate contextual biosafety and sustainability feedback"""
        category_emissions = footprint_breakdown.get(category, 0)
        total = footprint_breakdown.get("total", 1)
        percentage = (category_emissions / total * 100) if total > 0 else 0
        
        feedbacks = {
            "energy": f"Energy consumption accounts for {percentage:.1f}% of your carbon footprint. "
                     f"Transitioning to renewable energy sources and improving efficiency can significantly reduce your impact.",
            "transportation": f"Transportation represents {percentage:.1f}% of your emissions. "
                            f"Optimizing travel patterns and choosing low-carbon transport options offers substantial reduction potential.",
            "waste": f"Waste management contributes {percentage:.1f}% to your footprint. "
                    f"Implementing circular economy principles and waste reduction strategies will improve your sustainability profile.",
            "food": f"Food-related emissions make up {percentage:.1f}% of your carbon footprint. "
                   f"Dietary choices have significant environmental impact, with plant-based options offering much lower emissions.",
            "water": f"Water usage accounts for {percentage:.1f}% of your footprint. "
                    f"While smaller, efficient water management supports overall sustainability goals.",
            "corporate": f"Corporate operations contribute significantly to your footprint. "
                        f"Systematic changes in operations, supply chains, and employee practices can drive substantial improvements.",
            "general": "Every reduction counts. Small changes in daily habits compound into significant environmental benefits over time."
        }
        
        return feedbacks.get(category, feedbacks["general"])

