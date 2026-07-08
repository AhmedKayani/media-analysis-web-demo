const confidenceFill = document.getElementById("confidenceFill")
const previewContainer = document.getElementById("previewContainer")
const imagePreview = document.getElementById("imagePreview")
const imageInput = document.getElementById("imageInput")
const ImgAnalyzebtn = document.getElementById("ImgAnalyzebtn")
const audioInput = document.getElementById("audioInput")
const AudioAnalyzebtn = document.getElementById("AudioAnalyzebtn")
const statusText = document.getElementById("statusText")
const resultCard = document.getElementById("resultCard")

AudioAnalyzebtn.addEventListener("click", async () => {
  const file = audioInput.files[0]
})

imageInput.addEventListener("change", () => {
  const file = imageInput.files[0]

  if (!file) {
    previewContainer.classList.add("hidden")
    imagePreview.src = ""
    return
  }

  imagePreview.src = URL.createObjectURL(file)
  previewContainer.classList.remove("hidden")
  statusText.textContent = ""
  resultCard.classList.add("hidden")
})

ImgAnalyzebtn.addEventListener("click", async () => {
  const file = imageInput.files[0]
  confidenceFill.style.width = "0%"

  if (!file) {
    statusText.textContent = "Please select an image file."
    return
  }

  const formData = new FormData()
  formData.append("file", file)

  statusText.textContent = "Analyzing image"
  resultCard.classList.add("hidden")

  try {
    const response = await fetch("http://localhost:8000/analyze-image", {
      method: "POST",
      body: formData,
    })

    const data = await response.json()

    if (!response.ok) {
      statusText.textContent = "Error analyzing image."
      return
    }

    document.getElementById("filename").textContent = data.filename
    document.getElementById("contentType").textContent = data.content_type
    document.getElementById("fileSize").textContent = data.file_size_kb
    document.getElementById("prediction").textContent = data.prediction
    document.getElementById("confidence").textContent = data.confidence
    confidenceFill.style.width = `${data.confidence}%`
    document.getElementById("message").textContent = data.message
    statusText.textContent = "Analysis complete."

    resultCard.classList.remove("hidden")
  } catch (error) {
    statusText.textContent = "Could not connect to the backend."
  }
})
