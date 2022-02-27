from fastapi import HTTPException, status

DONE_ACTION = HTTPException(status_code=status.HTTP_200_OK)
NOT_FOUND = HTTPException(status_code=status.HTTP_404_NOT_FOUND)
CREATE_ACTION = HTTPException(status_code=status.HTTP_201_CREATED)
EXISTS_ACTION = HTTPException(status_code=status.HTTP_409_CONFLICT)
