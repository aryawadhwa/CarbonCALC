"""
Initialize the database with tables and sample data
"""
from database.database import init_db, SessionLocal
from database.models import IndustryBenchmark, UserType

def create_sample_benchmarks():
    """Create sample industry benchmarks"""
    db = SessionLocal()
    try:
        # Check if benchmarks already exist
        existing = db.query(IndustryBenchmark).first()
        if existing:
            print("Benchmarks already exist. Skipping...")
            return
        
        benchmarks = [
            IndustryBenchmark(
                industry_type="technology",
                user_type=UserType.CORPORATION,
                average_carbon_per_person=2500,
                average_carbon_total=250000,
                benchmark_year=2024
            ),
            IndustryBenchmark(
                industry_type="manufacturing",
                user_type=UserType.CORPORATION,
                average_carbon_per_person=8000,
                average_carbon_total=800000,
                benchmark_year=2024
            ),
            IndustryBenchmark(
                industry_type="healthcare",
                user_type=UserType.INSTITUTION,
                average_carbon_per_person=3000,
                average_carbon_total=300000,
                benchmark_year=2024
            ),
            IndustryBenchmark(
                industry_type="education",
                user_type=UserType.INSTITUTION,
                average_carbon_per_person=2000,
                average_carbon_total=200000,
                benchmark_year=2024
            ),
            IndustryBenchmark(
                industry_type="individual",
                user_type=UserType.INDIVIDUAL,
                average_carbon_per_person=4000,
                average_carbon_total=4000,
                benchmark_year=2024
            ),
        ]
        
        for benchmark in benchmarks:
            db.add(benchmark)
        
        db.commit()
        print("Sample industry benchmarks created successfully!")
    except Exception as e:
        print(f"Error creating benchmarks: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialized!")
    
    print("Creating sample benchmarks...")
    create_sample_benchmarks()
    print("Done!")

