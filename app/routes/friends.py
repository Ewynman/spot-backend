from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models
from ..db import get_db
from ..auth import get_current_user

router = APIRouter()

# ---------------------------------------------
# ✅ Send a Friend Request
# ---------------------------------------------
@router.post("/friends/request/{user_id}")
def send_friend_request(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # 🔐 Prevent sending request to yourself
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="You cannot send a friend request to yourself")

    # 🧍‍♂️ Check if target user exists
    target_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    # 🔁 Check if a pending request already exists
    existing_request = db.query(models.FriendRequest).filter_by(
        from_user_id=current_user.id,
        to_user_id=user_id,
        status="pending"
    ).first()

    if existing_request:
        raise HTTPException(status_code=400, detail="Friend request already sent")

    # ✅ Create and save new friend request
    friend_request = models.FriendRequest(
        from_user_id=current_user.id,
        to_user_id=user_id,
        status="pending"
    )
    db.add(friend_request)
    db.commit()
    db.refresh(friend_request)

    return {"message": "Friend request sent"}

# ---------------------------------------------
# ✅ Respond to a Friend Request
# ---------------------------------------------
@router.post("/friends/respond/{request_id}")
def respond_to_friend_request(
    request_id: int,
    action: str,  # either "accept" or "reject"
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # 🔎 Fetch the friend request
    request = db.query(models.FriendRequest).filter_by(
        id=request_id,
        to_user_id=current_user.id
    ).first()

    if not request:
        raise HTTPException(status_code=404, detail="Friend request not found")

    if request.status != "pending":
        raise HTTPException(status_code=400, detail="This request has already been handled")

    if action == "accept":
        # ✅ Update request status
        request.status = "accepted"

        # 🤝 Create mutual follower relationships
        stmt1 = models.followers.insert().values(
            follower_id=current_user.id, followed_id=request.from_user_id
        )
        stmt2 = models.followers.insert().values(
            follower_id=request.from_user_id, followed_id=current_user.id
        )
        db.execute(stmt1)
        db.execute(stmt2)

    elif action == "reject":
        request.status = "rejected"
    else:
        raise HTTPException(status_code=400, detail="Invalid action")

    db.commit()
    return {"message": f"Friend request {action}ed"}

# -------------------------------
# List all friend requests (incoming + outgoing)
# -------------------------------
@router.get("/friends/requests")
def get_friend_requests(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # All requests sent to the current user (they need to respond)
    incoming = db.query(models.FriendRequest).filter(
        models.FriendRequest.to_user_id == current_user.id
    ).all()

    # All requests sent by the current user (waiting for others to respond)
    outgoing = db.query(models.FriendRequest).filter(
        models.FriendRequest.from_user_id == current_user.id
    ).all()

    return {
        "incoming": [
            {
                "request_id": req.id,
                "from_user_id": req.from_user_id,
                "status": req.status,
                "sent_at": req.created_at
            } for req in incoming
        ],
        "outgoing": [
            {
                "request_id": req.id,
                "to_user_id": req.to_user_id,
                "status": req.status,
                "sent_at": req.created_at
            } for req in outgoing
        ]
    }


