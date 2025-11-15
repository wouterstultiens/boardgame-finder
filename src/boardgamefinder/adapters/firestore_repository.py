# src/boardgamefinder/adapters/firestore_repository.py
import hashlib
from datetime import datetime, timezone
from typing import List, Optional
from google.cloud import firestore

from ..domain.models import Listing

class ListingRepository:
    """Manages persistence of Listing objects in Firestore."""

    _COLLECTION = "listings"

    def __init__(self, client: firestore.Client):
        self._client = client
        self._collection = self._client.collection(self._COLLECTION)
        print("Firestore ListingRepository initialized.")

    def _doc_id_from_link(self, link: str) -> str:
        """Generates a consistent document ID from a URL."""
        return hashlib.sha256(link.encode("utf-8")).hexdigest()[:20]

    def find_by_link(self, link: str) -> Optional[Listing]:
        """Finds a listing by its Marktplaats URL."""
        doc_id = self._doc_id_from_link(link)
        snap = self._collection.document(doc_id).get()
        return Listing.model_validate(snap.to_dict()) if snap.exists else None

    def get_all(self) -> List[Listing]:
        """Retrieves all listings from the collection."""
        listings = []
        for doc in self._collection.stream():
            try:
                listings.append(Listing.model_validate(doc.to_dict()))
            except Exception as e:
                print(f"Failed to validate listing {doc.id}: {e}")
        return listings

    def save(self, listing: Listing) -> None:
        """Saves a listing to Firestore, setting timestamps."""
        doc_id = self._doc_id_from_link(str(listing.link))
        now = datetime.now(timezone.utc)

        # Check if the document exists to set created_at only once
        doc_ref = self._collection.document(doc_id)
        existing_doc = doc_ref.get()

        listing.updated_at = now
        if not existing_doc.exists:
            listing.created_at = now

        data = listing.model_dump(mode="json")
        doc_ref.set(data, merge=True)
        print(f"Saved listing {doc_id} for URL: {listing.link}")

def get_listing_repository() -> ListingRepository:
    """Factory function to get a configured ListingRepository instance."""
    client = firestore.Client(project=settings.gcp_project_id)
    return ListingRepository(client=client)