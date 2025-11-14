from __future__ import annotations
import hashlib
from datetime import datetime, timezone
from typing import Optional

from google.cloud import firestore
from .models import Listing

_client = firestore.Client()
_COLLECTION = "listings"


def _doc_id_from_link(link: str) -> str:
    return hashlib.sha256(link.encode("utf-8")).hexdigest()[:16]


def get_listing_by_link(link: str) -> Optional[Listing]:
    doc_id = _doc_id_from_link(link)
    snap = _client.collection(_COLLECTION).document(doc_id).get()
    if not snap.exists:
        return None
    return Listing.model_validate(snap.to_dict())


def save_listing(listing: Listing) -> None:
    now = datetime.now(timezone.utc)

    doc_id = _doc_id_from_link(str(listing.link))
    data = listing.model_dump(mode="json")
    data.setdefault("created_at", now.isoformat())
    data["updated_at"] = now.isoformat()

    _client.collection(_COLLECTION).document(doc_id).set(data, merge=True)
