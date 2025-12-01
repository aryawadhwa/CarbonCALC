"""
Comparative Benchmarking and Industry Analysis
Research-grade comparison against industry standards and peers
"""
from typing import Dict, List, Optional
from database.models import IndustryBenchmark, UserType
from sqlalchemy.orm import Session
import statistics


class BenchmarkAnalyzer:
    """Analyze and compare carbon footprints against industry benchmarks"""
    
    @staticmethod
    def compare_with_benchmark(
        user_footprint: float,
        user_type: UserType,
        employee_count: int,
        db: Session,
        industry_type: Optional[str] = None
    ) -> Dict:
        """
        Compare user's footprint against industry benchmarks
        Returns comprehensive comparison metrics
        """
        # Get relevant benchmarks
        query = db.query(IndustryBenchmark).filter(
            IndustryBenchmark.user_type == user_type
        )
        
        if industry_type:
            query = query.filter(IndustryBenchmark.industry_type == industry_type)
        
        benchmarks = query.all()
        
        if not benchmarks:
            return {"error": "No benchmarks available for comparison"}
        
        # Calculate per-person footprint
        per_person_footprint = user_footprint / employee_count if employee_count > 0 else user_footprint
        
        # Aggregate benchmark statistics
        benchmark_per_person = [b.average_carbon_per_person for b in benchmarks]
        benchmark_totals = [b.average_carbon_total for b in benchmarks]
        
        avg_benchmark_per_person = statistics.mean(benchmark_per_person)
        median_benchmark_per_person = statistics.median(benchmark_per_person)
        
        # Calculate percentiles
        benchmark_per_person_sorted = sorted(benchmark_per_person)
        if len(benchmark_per_person_sorted) > 0:
            percentile_25 = benchmark_per_person_sorted[len(benchmark_per_person_sorted) // 4]
            percentile_75 = benchmark_per_person_sorted[3 * len(benchmark_per_person_sorted) // 4]
        else:
            percentile_25 = percentile_75 = avg_benchmark_per_person
        
        # Comparison metrics
        deviation_from_mean = per_person_footprint - avg_benchmark_per_person
        percentage_deviation = (deviation_from_mean / avg_benchmark_per_person * 100) if avg_benchmark_per_person > 0 else 0
        
        # Performance rating
        if per_person_footprint <= percentile_25:
            performance_rating = "excellent"
            performance_score = 5
        elif per_person_footprint <= median_benchmark_per_person:
            performance_rating = "good"
            performance_score = 4
        elif per_person_footprint <= percentile_75:
            performance_rating = "average"
            performance_score = 3
        elif per_person_footprint <= avg_benchmark_per_person * 1.2:
            performance_rating = "below_average"
            performance_score = 2
        else:
            performance_rating = "poor"
            performance_score = 1
        
        # Improvement potential
        improvement_potential = max(0, per_person_footprint - percentile_25) * employee_count
        
        return {
            "user_footprint": {
                "total_kg_co2": round(user_footprint, 2),
                "per_person_kg_co2": round(per_person_footprint, 2),
                "employee_count": employee_count
            },
            "industry_benchmarks": {
                "average_per_person": round(avg_benchmark_per_person, 2),
                "median_per_person": round(median_benchmark_per_person, 2),
                "percentile_25": round(percentile_25, 2),
                "percentile_75": round(percentile_75, 2),
                "sample_size": len(benchmarks)
            },
            "comparison": {
                "deviation_kg_co2": round(deviation_from_mean, 2),
                "percentage_deviation": round(percentage_deviation, 2),
                "performance_rating": performance_rating,
                "performance_score": performance_score,
                "comparison_status": "better" if deviation_from_mean < 0 else "worse" if deviation_from_mean > 0 else "equal"
            },
            "improvement_potential": {
                "potential_reduction_kg_co2": round(improvement_potential, 2),
                "target_per_person_kg_co2": round(percentile_25, 2),
                "reduction_percentage": round((improvement_potential / user_footprint * 100) if user_footprint > 0 else 0, 2)
            },
            "research_metrics": {
                "benchmark_coverage": len(benchmarks),
                "statistical_significance": "high" if len(benchmarks) >= 10 else "moderate" if len(benchmarks) >= 5 else "low",
                "comparison_methodology": "industry_standard_percentile_analysis"
            }
        }
    
    @staticmethod
    def generate_comparative_report(
        user_entries: List[Dict],
        benchmarks: List[IndustryBenchmark],
        user_type: UserType
    ) -> Dict:
        """
        Generate comprehensive comparative research report
        """
        if not user_entries:
            return {"error": "No user data available"}
        
        # Calculate user statistics
        footprints = [e.get('total_carbon_footprint', 0) for e in user_entries]
        
        user_stats = {
            "mean": statistics.mean(footprints),
            "median": statistics.median(footprints),
            "std_dev": statistics.stdev(footprints) if len(footprints) > 1 else 0,
            "min": min(footprints),
            "max": max(footprints),
            "sample_size": len(footprints)
        }
        
        # Benchmark statistics
        benchmark_footprints = [b.average_carbon_per_person for b in benchmarks]
        
        benchmark_stats = {
            "mean": statistics.mean(benchmark_footprints),
            "median": statistics.median(benchmark_footprints),
            "std_dev": statistics.stdev(benchmark_footprints) if len(benchmark_footprints) > 1 else 0,
            "min": min(benchmark_footprints),
            "max": max(benchmark_footprints),
            "sample_size": len(benchmark_footprints)
        }
        
        # Statistical comparison
        effect_size = (user_stats["mean"] - benchmark_stats["mean"]) / benchmark_stats["std_dev"] if benchmark_stats["std_dev"] > 0 else 0
        
        return {
            "user_statistics": {k: round(v, 2) if isinstance(v, float) else v for k, v in user_stats.items()},
            "benchmark_statistics": {k: round(v, 2) if isinstance(v, float) else v for k, v in benchmark_stats.items()},
            "statistical_analysis": {
                "effect_size": round(effect_size, 3),
                "effect_interpretation": "large" if abs(effect_size) > 0.8 else "medium" if abs(effect_size) > 0.5 else "small",
                "user_vs_benchmark": "higher" if effect_size > 0 else "lower" if effect_size < 0 else "equivalent"
            },
            "research_quality": {
                "user_sample_size": len(footprints),
                "benchmark_sample_size": len(benchmarks),
                "comparison_validity": "high" if len(footprints) >= 5 and len(benchmarks) >= 5 else "moderate"
            }
        }

