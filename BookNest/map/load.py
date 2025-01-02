from pathlib import Path
import csv
from map.models import Book

csv_path = Path("map/data/goodreads_data.csv")

def run(verbose=True):

    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            Book.objects.create(
                title=row["Book"],
                author=row["Author"],
                description=row["Description"],
                genres=row["Genres"],
                avg_rating=float(row["Avg_Rating"]) if row["Avg_Rating"] else None,
                num_ratings=int(row["Num_Ratings"].replace(",", "")) if row["Num_Ratings"] else None,
                book_url=row["URL"],
            )