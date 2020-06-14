import http from "../http-common";

class ApiService {
  upload_file(file, onUploadProgress) {
    let formData = new FormData();

    formData.append("file", file);

    return http.post("/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
      onUploadProgress,
    });
  }
  upload(title, content) {
    return http.post(`/text/save/${title}`, content, {
      headers: {
        "Content-Type": "application/json",
      },
    });
  }
  getTexts() {
    return http.get("/text");
  }
  getTextLinesById(id) {
    return http.get(`/text/lines/${id}`);
  }
  getSimilarLines(lineId) {
    return http.get(`/text/similar/${lineId}`);
  }
}

export default new ApiService();
