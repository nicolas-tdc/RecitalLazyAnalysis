# RecitalLazyAnalysis (WIP)
This API is used to analyse files (text, pdf and images) comparing word frequencies in the file's text with Zipf's Law's predictions.

Created using FastAPI, SQLAlchemy and Celery.

---

Models :

  - FileImport : Name and text content of the file.

  - TextAnalysis : ID of the file analysed and differences (numeric and percentage) with Zipf's Law's predictions.

---

Views:

  - Upload form for multiple files : /analysis/
  
  - Action for upload form with FileImport and TextAnalysis creation through celery task. /files-import/

  - Single and lists for each model : /files/{file_id} - /files/ - /analysis/{analysis_id} - /analysis/
