from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import Response
from typing import List
from src.services.method import MethodsService

from src.services.authorization import get_current_user_data


router = APIRouter(
    prefix='/methods',
    tags=['methods'],
    dependencies=[Depends(get_current_user_data)]
)


@router.post("/dataProcessing", name="Обработка данных")
def data_processing(file: UploadFile, methods_service: MethodsService = Depends(), user_data: List = Depends(get_current_user_data)):
    out = methods_service.data_processing(user_data[0], file.file)
    return Response(out, media_type='text/csv',
                             headers={"Content-Disposition": "attachment; filename=proceeded_data.csv",
                                      "Content-Type": "text/csv"})


@router.post("/fit", status_code=status.HTTP_200_OK, name="Обучение модели")
def fit(file: UploadFile, methods_service: MethodsService = Depends(), user_data: List = Depends(get_current_user_data)):
    return methods_service.fit(user_data[0], file.file)


@router.post("/predict", name="Предсказание модели")
def predict(file: UploadFile, methods_service: MethodsService = Depends(), user_data: List = Depends(get_current_user_data)):
    out = methods_service.predict(user_data[0], file.file)
    return Response(out, media_type='text/csv',
                             headers={"Content-Disposition": "attachment; filename=predict_data.csv",
                                      "Content-Type": "text/csv"})


@router.post("/download", name="Скачать данные")
def download(methods_service: MethodsService = Depends(), user_data: List = Depends(get_current_user_data)):
    out = methods_service.download(user_data[0])
    return Response(out, media_type='text/csv',
                             headers={"Content-Disposition": "attachment; filename=train_data.csv",
                                      "Content-Type": "text/csv"})
