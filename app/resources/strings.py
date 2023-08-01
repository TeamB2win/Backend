### API message resource 관리

DATA_NOT_FOUND = "data doesn't exist in database."
ID_NOT_FOUND = "id data doesn't exist in database."
INVAILD_FILE = "file not found in given path"

VIDEO_PATH_ALREADY_EXIST = "video path is already exist in database. if you want to change video url resource try PUT method alternatively."
VIDEO_PATH_NOT_EXIST = "video path is not exist in database. if you want to create video url resource try POST method alternatively."

IMAGE_NOT_WRITABLE = "Can't write the image"
IMAGE_NOT_OPEN_BY_IMAGEIO = "Can't open image by using image framework(imageio)"

DB_DL_PROCESS_NOT_COMPLETED = "Image and DB process on the server is not completed"
DB_PROCESS_NOT_COMPLETED = "DB process on the server is not completed"

### API Docs Error Description 관리

DESCRIPTION_400_ERROR_FOR_DATA_FILE = "해당되는 파일 경로를 서버에서 인식할 수 없습니다."
DESCRIPTION_400_ERROR = "요청의 오류로 데이터베이스 쿼리 작업을 수행하지 못했습니다."
DESCRIPTION_404_ERROR = "해당하는 데이터가 데이터베이스에 존재하지 않습니다."
DESCRIPTION_415_ERROR = "전송한 파일이 지원하지 않는 형식입니다."