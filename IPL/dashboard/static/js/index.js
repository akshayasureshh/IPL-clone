const image=document.getElementById('image')
const cropper=new Cropper(image,{
    aspectRatio:1,
    viewMode:0,
})

document.getElementById('cropImageBtn').addEventListener('click',
function(){
        var croppedImage=cropper.getCroppedCanvas().toDataURL("boy/png")
        document.getElementById('output').src=croppedImage
})