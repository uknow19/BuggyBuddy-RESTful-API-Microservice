from src.core.usecases.report_crud_usecase import ReportCRUDUsecase
from src.core.usecases.report_vectorize_usecase import ReportVectorizeUsecase

from src.infrastructure.main_drivers.report_crud_operator_driver import ReportCRUDOperatorDriver
from src.infrastructure.main_drivers.report_preprocessor_driver import ReportPreprocessorDriver
from src.infrastructure.main_drivers.revectorizer_driver import RevectorizerDriver

from src.infrastructure.logger.logger_driver import LoggerDriver

from src.infrastructure.api.routes import api_routers

from pinecone import Pinecone
from fastapi import FastAPI, APIRouter

app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})
router = APIRouter()
logger_driver = LoggerDriver()

def crud_usecase_builder():
  try:
    pc = Pinecone(api_key='d5532e31-0f59-48ce-a12a-743f75e16b5f')
    pc_index = pc.Index('bug-report-index')
    
    report_preprocessor_driver = ReportPreprocessorDriver(logger_driver)
    revectorizer_driver = RevectorizerDriver(logger_driver)
    report_crud_operator_driver = ReportCRUDOperatorDriver(pc_index, logger_driver)
    
    report_vectorize_usecase = ReportVectorizeUsecase(
      report_preprocessor=report_preprocessor_driver,
      revectorizer=revectorizer_driver,
      logger=logger_driver)
    report_crud_usecase = ReportCRUDUsecase(
      report_crud_operator=report_crud_operator_driver,
      report_vectorize_usecase=report_vectorize_usecase,
      logger=logger_driver)
    
    return report_crud_usecase
  except Exception as error:
    error_message = f'main:crud_usecase_builder: {error}'
    logger_driver.log_error(error_message, error)

report_crud_usecase = crud_usecase_builder()
api_routes = api_routers(router, report_crud_usecase)
app.include_router(api_routes)
  

