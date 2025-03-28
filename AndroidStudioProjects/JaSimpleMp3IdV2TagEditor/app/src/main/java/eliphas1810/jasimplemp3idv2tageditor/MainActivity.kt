package eliphas1810.jasimplemp3idv2tageditor

import android.content.Intent
import android.graphics.BitmapFactory
import android.net.Uri
import android.os.Bundle
import android.widget.*
import androidx.activity.result.ActivityResult
import androidx.activity.result.ActivityResultLauncher
import androidx.activity.result.contract.ActivityResultContracts.StartActivityForResult
import androidx.appcompat.app.AppCompatActivity
import androidx.documentfile.provider.DocumentFile
import java.io.BufferedOutputStream
import java.nio.charset.Charset
import java.nio.charset.StandardCharsets
import kotlin.experimental.and

class MainActivity : AppCompatActivity() {


    var titleEditText: EditText? = null
    var artistEditText: EditText? = null
    var albumEditText: EditText? = null
    var trackEditText: EditText? = null

    var jacketImageView: ZoomableImageView? = null

    var imageMimetype: String? = null
    var imageByteArray: ByteArray? = null
    var mpegFrameByteArray: ByteArray? = null


    private var selectMP3ActivityResultLauncher: ActivityResultLauncher<Intent>? = registerForActivityResult(StartActivityForResult()) { activityResult: ActivityResult ->

        if (activityResult.resultCode == RESULT_OK) {
            val intent = activityResult.data

            val uri: Uri? = intent?.data

            val documentFile = DocumentFile.fromSingleUri(applicationContext, uri!!)

            val fileName: String? = documentFile?.name

            if ((fileName?.matches(Regex("^.+\\.[mM][pP]3$")) ?: false) == false) {
                Toast.makeText(applicationContext, getString(R.string.select_mp3_message), Toast.LENGTH_LONG).show()
                return@registerForActivityResult
            }

            var byteArray = ByteArray(0)
            contentResolver.openInputStream(uri!!).use {
                byteArray = it?.readBytes() ?: ByteArray(0) //2GB以下しか読み込めません。
            }

            titleEditText?.setText("")
            artistEditText?.setText("")
            albumEditText?.setText("")
            trackEditText?.setText("")

            jacketImageView?.setImageBitmap(null)

            imageMimetype = null
            imageByteArray = null
            mpegFrameByteArray = null

            val id3: String = String(byteArray.sliceArray(0..2), StandardCharsets.UTF_8)
            if (id3 != "ID3") {
                mpegFrameByteArray = byteArray
                return@registerForActivityResult
            }

            val minorVersion: Int = byteArray[3].toInt()
            if (minorVersion <= 2 || 5 <= minorVersion) {
                Toast.makeText(applicationContext, getString(R.string.not_support_version_message), Toast.LENGTH_LONG).show()
                return@registerForActivityResult
            }

            //int batchVersion = byteArray[4].toInt()

            val flag: Byte = byteArray[5]
            val hasExHeader: Boolean = flag.and(0x02).toInt() != 0
            var headerSize: Int = 0
            headerSize += byteArray[6].toInt().shl(21)
            headerSize += byteArray[7].toInt().shl(14)
            headerSize += byteArray[8].toInt().shl(7)
            headerSize += byteArray[9].toInt()

            var byteIndex: Int = 10

            if (hasExHeader) {
                var exHeaderSize: Int = 0
                if (minorVersion == 3) {
                    exHeaderSize += byteArray[10].toInt().shl(24)
                    exHeaderSize += byteArray[11].toInt().shl(16)
                    exHeaderSize += byteArray[12].toInt().shl(8)
                    exHeaderSize += byteArray[13]
                } else {
                    exHeaderSize += byteArray[10].toInt().shl(21)
                    exHeaderSize += byteArray[11].toInt().shl(14)
                    exHeaderSize += byteArray[12].toInt().shl(7)
                    exHeaderSize += byteArray[13]
                }
                byteIndex += exHeaderSize
            }

            while (byteIndex < headerSize) {

                val frameId: String = String(byteArray.sliceArray(byteIndex..(byteIndex + 3)), StandardCharsets.UTF_8)
                byteIndex += 4

                if (byteIndex == 14 && frameId.matches(Regex("^[A-Z][A-Z][A-Z][A-Z0-9]$")) == false) {
                    byteIndex -= 4
                    var exHeaderSize: Int = 0
                    if (minorVersion == 3) {
                        exHeaderSize += byteArray[10].toInt().shl(24)
                        exHeaderSize += byteArray[11].toInt().shl(16)
                        exHeaderSize += byteArray[12].toInt().shl(8)
                        exHeaderSize += byteArray[13]
                    } else {
                        exHeaderSize += byteArray[10].toInt().shl(21)
                        exHeaderSize += byteArray[11].toInt().shl(14)
                        exHeaderSize += byteArray[12].toInt().shl(7)
                        exHeaderSize += byteArray[13]
                    }
                    byteIndex += exHeaderSize
                    continue
                }

                var frameSize: Int = 0
                if (minorVersion == 3) {
                    frameSize += byteArray[byteIndex].toInt().shl(24)
                    frameSize += byteArray[byteIndex + 1].toInt().shl(16)
                    frameSize += byteArray[byteIndex + 2].toInt().shl(8)
                    frameSize += byteArray[byteIndex + 3].toInt()
                } else {
                    frameSize += byteArray[byteIndex].toInt().shl(21)
                    frameSize += byteArray[byteIndex + 1].toInt().shl(14)
                    frameSize += byteArray[byteIndex + 2].toInt().shl(7)
                    frameSize += byteArray[byteIndex + 3].toInt()
                }
                byteIndex += 4

                byteIndex += 2 //フレームのフラグは無視して飛ばします。

                if (frameId.matches(Regex("^TIT2$|^TPE1$|^TALB$|^TRCK$"))) {

                    val encodingByte: Byte = byteArray[byteIndex]
                    var charset: Charset? = null
                    if (encodingByte.toInt() == 0x00) {
                        //charset = Charset.forName("ISO-8859-1")
                        charset = Charset.forName("Windows-31J") //過去の日本語のアプリケーションにはISO-8859-1でWindowsの日本語のテキストを書き込んでいた物が有ったそうです。
                    } else if (encodingByte.toInt() == 0x01) {
                        charset = Charset.forName("UTF-16")
                    } else if (minorVersion == 4 && encodingByte.toInt() == 0x02) {
                        charset = Charset.forName("UTF-16BE")
                    } else if (minorVersion == 4 && encodingByte.toInt() == 0x03) {
                        charset = Charset.forName("UTF-8")
                    } else {
                        Toast.makeText(applicationContext, getString(R.string.invalid_text_encoding_message) + " Minor Version: " + minorVersion + " Text Encoding Byte: " + encodingByte.toInt(), Toast.LENGTH_LONG).show()
                        return@registerForActivityResult
                    }
                    byteIndex += 1

                    val content = String(byteArray.sliceArray(byteIndex..(byteIndex + frameSize - 2)), charset)
                    byteIndex += (frameSize - 1)

                    if (frameId == "TIT2") {
                        titleEditText?.setText(content)
                    } else if (frameId == "TPE1") {
                        artistEditText?.setText(content)
                    } else if (frameId == "TALB") {
                        albumEditText?.setText(content)
                    } else if (frameId == "TRCK") {
                        trackEditText?.setText(content)
                    }

                } else if (frameId == "APIC") {

                    val encodingByte: Byte = byteArray[byteIndex]
                    var charset: Charset? = null
                    if (encodingByte.toInt() == 0x00) {
                        //charset = Charset.forName("ISO-8859-1")
                        charset = Charset.forName("Windows-31J") //過去の日本語のアプリケーションにはISO-8859-1でWindowsの日本語のテキストを書き込んでいた物が有ったそうです。
                    } else if (encodingByte.toInt() == 0x01) {
                        charset = Charset.forName("UTF-16")
                    } else if (minorVersion == 4 && encodingByte.toInt() == 0x02) {
                        charset = Charset.forName("UTF-16BE")
                    } else if (minorVersion == 4 && encodingByte.toInt() == 0x03) {
                        charset = Charset.forName("UTF-8")
                    } else {
                        Toast.makeText(applicationContext, getString(R.string.invalid_text_encoding_message) + " Minor Version: " + minorVersion + " Text Encoding Byte: " + encodingByte.toInt(), Toast.LENGTH_LONG).show()
                        return@registerForActivityResult
                    }
                    byteIndex += 1

                    val mimetypeByteList: MutableList<Byte> = mutableListOf()
                    for (index in 0..(frameSize - 2)) {
                        val currentByte: Byte = byteArray[byteIndex + index]
                        if (currentByte.toInt() == 0x00/* NULL */) {
                            break
                        }
                        mimetypeByteList.add(currentByte)
                    }
                    imageMimetype = String(mimetypeByteList.toByteArray(), charset)
                    byteIndex += (mimetypeByteList.size + 1)

                    byteIndex += 1 //Picture Type(画像の種類)を無視して飛ばします。

                    val descriptionList: MutableList<Byte> = mutableListOf()
                    for (index in 0..(frameSize - 1 - mimetypeByteList.size - 1 - 1 - 1)) {
                        val currentByte: Byte = byteArray[byteIndex + index]
                        if (currentByte.toInt() == 0x00/* NULL */) {
                            break
                        }
                        descriptionList.add(currentByte)
                    }
                    byteIndex += (descriptionList.size + 1)

                    imageByteArray = byteArray.sliceArray(byteIndex..(byteIndex + frameSize - 1 - mimetypeByteList.size - 1 - 1 - descriptionList.size - 1 - 1))

                    jacketImageView?.setImageBitmap(BitmapFactory.decodeByteArray(imageByteArray, 0, imageByteArray!!.size))

                } else {
                    byteIndex += frameSize
                }
            }

            if (headerSize < byteIndex) {
                byteIndex = headerSize
            }

            mpegFrameByteArray = byteArray.sliceArray(byteIndex..(byteIndex + byteArray.size - headerSize - 1))
        }
    }


    private var selectJacketImageActivityResultLauncher: ActivityResultLauncher<Intent>? = registerForActivityResult(StartActivityForResult()) { activityResult: ActivityResult ->

        if (activityResult.resultCode == RESULT_OK) {
            val intent = activityResult.data

            val uri: Uri? = intent?.data

            val documentFile = DocumentFile.fromSingleUri(applicationContext, uri!!)

            val fileName: String? = documentFile?.name

            if ((fileName?.matches(Regex("^.+\\.[pP][nN][gG]$|^.+\\.[jJ][pP][eE]?[gG]$")) ?: false) == false) {
                Toast.makeText(applicationContext, getString(R.string.select_png_or_jpeg_message), Toast.LENGTH_LONG).show()
                return@registerForActivityResult
            }

            if (fileName?.matches(Regex("^.+\\.[pP][nN][gG]$")) ?: false) {
                imageMimetype = "image/png"
            } else {
                imageMimetype = "image/jpeg"
            }

            contentResolver.openInputStream(uri!!).use {
                imageByteArray = it?.readBytes() ?: ByteArray(0) //2GB以下しか読み込めません。
            }

            jacketImageView?.setImageBitmap(BitmapFactory.decodeByteArray(imageByteArray, 0, imageByteArray!!.size))
        }
    }


    private var makeMP3ActivityResultLauncher: ActivityResultLauncher<Intent>? = registerForActivityResult(StartActivityForResult()) { activityResult: ActivityResult ->

        if (activityResult.resultCode == RESULT_OK) {
            val intent = activityResult.data
            val uri: Uri? = intent?.data

            if (mpegFrameByteArray?.isEmpty() ?: false) {
                Toast.makeText(applicationContext, getString(R.string.select_mp3_message), Toast.LENGTH_LONG).show()
                return@registerForActivityResult
            }

            val title = titleEditText?.getText()?.toString() ?: ""
            val artist = artistEditText?.getText()?.toString() ?: ""
            val album = albumEditText?.getText()?.toString() ?: ""
            val track = trackEditText?.getText()?.toString() ?: ""

            //contentResolver.openOutputStream()で"wt"モードを指定しないと、書き込み前のバイト数が大きい場合、書き込み前のバイトの先頭の一部を置換するような形に成ってしまいます。
            BufferedOutputStream(contentResolver.openOutputStream(uri!!, "wt")).use {

                val titleByteArray = title.toByteArray(StandardCharsets.UTF_16)
                val artistByteArray = artist.toByteArray(StandardCharsets.UTF_16)
                val albumByteArray = album.toByteArray(StandardCharsets.UTF_16)
                val trackByteArray = track.toByteArray(StandardCharsets.UTF_16)

                var headerSize: Int = 0
                headerSize += 10
                headerSize += (10 + 1 + titleByteArray.size)
                headerSize += (10 + 1 + artistByteArray.size)
                headerSize += (10 + 1 + trackByteArray.size)
                if (album.isEmpty() == false) {
                    headerSize += (10 + 1 + albumByteArray.size)
                }
                if (1 <= (imageByteArray?.size ?: 0)) {
                    headerSize += (10 + 1 + (imageMimetype?.length ?: 0) + 1 + 1 + 1 + (imageByteArray?.size ?: 0))
                }

                //Javaはデフォルトはビッグ エンディアン
                //ID3v2タグはビッグ エンディアン

                it?.write(0x49/* I */)
                it?.write(0x44/* D */)
                it?.write(0x33/* 3 */)
                it?.write(0x03/* マイナーバージョン3 */)
                it?.write(0x00/* パッチバージョン0 */)
                it?.write(0x00/* ヘッダーのフラグ */)
                it?.write(headerSize.shl(4).ushr(25))
                it?.write(headerSize.shl(11).ushr(25))
                it?.write(headerSize.shl(18).ushr(25))
                it?.write(headerSize.shl(25).ushr(25))

                it?.write(0x54/* T */)
                it?.write(0x49/* I */)
                it?.write(0x54/* T */)
                it?.write(0x32/* 2 */)
                it?.write((1 + titleByteArray.size).ushr(24))
                it?.write((1 + titleByteArray.size).shl(8).ushr(24))
                it?.write((1 + titleByteArray.size).shl(16).ushr(24))
                it?.write((1 + titleByteArray.size).shl(24).ushr(24))
                it?.write(0x00/* フレームのフラグ */)
                it?.write(0x00/* フレームのフラグ */)
                it?.write(0x01/* テキストのフレームの文字コード。BOM付きUTF-16は16進数で01。 */)
                for (index in 0..(titleByteArray.size - 1)) {
                    it?.write(titleByteArray[index].toInt())
                }

                it?.write(0x54/* T */)
                it?.write(0x50/* P */)
                it?.write(0x45/* E */)
                it?.write(0x31/* 1 */)
                it?.write((1 + artistByteArray.size).ushr(24))
                it?.write((1 + artistByteArray.size).shl(8).ushr(24))
                it?.write((1 + artistByteArray.size).shl(16).ushr(24))
                it?.write((1 + artistByteArray.size).shl(24).ushr(24))
                it?.write(0x00/* フレームのフラグ */)
                it?.write(0x00/* フレームのフラグ */)
                it?.write(0x01/* テキストのフレームの文字コード。BOM付きUTF-16は16進数で01。 */)
                for (index in 0..(artistByteArray.size - 1)) {
                    it?.write(artistByteArray[index].toInt())
                }

                it?.write(0x54/* T */)
                it?.write(0x52/* R */)
                it?.write(0x43/* C */)
                it?.write(0x4B/* K */)
                it?.write((1 + trackByteArray.size).ushr(24))
                it?.write((1 + trackByteArray.size).shl(8).ushr(24))
                it?.write((1 + trackByteArray.size).shl(16).ushr(24))
                it?.write((1 + trackByteArray.size).shl(24).ushr(24))
                it?.write(0x00/* フレームのフラグ */)
                it?.write(0x00/* フレームのフラグ */)
                it?.write(0x01/* テキストのフレームの文字コード。BOM付きUTF-16は16進数で01。 */)
                for (index in 0..(trackByteArray.size - 1)) {
                    it?.write(trackByteArray[index].toInt())
                }

                if (album.isEmpty() == false) {
                    it?.write(0x54/* T */)
                    it?.write(0x41/* A */)
                    it?.write(0x4C/* L */)
                    it?.write(0x42/* B */)
                    it?.write((1 + albumByteArray.size).ushr(24))
                    it?.write((1 + albumByteArray.size).shl(8).ushr(24))
                    it?.write((1 + albumByteArray.size).shl(16).ushr(24))
                    it?.write((1 + albumByteArray.size).shl(24).ushr(24))
                    it?.write(0x00/* フレームのフラグ */)
                    it?.write(0x00/* フレームのフラグ */)
                    it?.write(0x01/* テキストのフレームの文字コード。BOM付きUTF-16は16進数で01。 */)
                    for (index in 0..(albumByteArray.size - 1)) {
                        it?.write(albumByteArray[index].toInt())
                    }
                }

                if (1 <= (imageByteArray?.size ?: 0)) {
                    it?.write(0x41/* A */)
                    it?.write(0x50/* P */)
                    it?.write(0x49/* I */)
                    it?.write(0x43/* C */)
                    it?.write((1 + (imageMimetype?.length ?: 0) + 1 + 1 + 1 + (imageByteArray?.size ?: 0)).ushr(24))
                    it?.write((1 + (imageMimetype?.length ?: 0) + 1 + 1 + 1 + (imageByteArray?.size ?: 0)).shl(8).ushr(24))
                    it?.write((1 + (imageMimetype?.length ?: 0) + 1 + 1 + 1 + (imageByteArray?.size ?: 0)).shl(16).ushr(24))
                    it?.write((1 + (imageMimetype?.length ?: 0) + 1 + 1 + 1 + (imageByteArray?.size ?: 0)).shl(24).ushr(24))
                    it?.write(0x00/* フレームのフラグ */)
                    it?.write(0x00/* フレームのフラグ */)
                    it?.write(0x00/* テキストのフレームの文字コード。ISO-8859-1は16進数で00。 */)

                    val imageMimetypeByteArray: ByteArray? = imageMimetype?.toByteArray(StandardCharsets.UTF_8) //UTF-8はISO-8859-1を包含

                    for (index in 0..((imageMimetypeByteArray?.size ?: 0) - 1)) {
                        it?.write(imageMimetypeByteArray!![index].toInt())
                    }

                    it?.write(0x00/* NULLの文字コード */)
                    it?.write(0x03/* Picture Type(画像の種類)。Front Cover(表カバー)は16進数で03。 */)
                    it?.write(0x00/* Description(説明)の終了を表すNULLの文字コード。 */)

                    for (index in 0..((imageByteArray?.size ?: 0) - 1)) {
                        it?.write(imageByteArray!![index].toInt())
                    }
                }

                for (index in 0..((mpegFrameByteArray?.size ?: 0) - 1)) {
                    it?.write(mpegFrameByteArray!![index].toInt())
                }

                it.flush()
            }

            Toast.makeText(applicationContext, getString(R.string.make_mp3_complete_message), Toast.LENGTH_LONG).show()
        }
    }


    override fun onCreate(savedInstanceState: Bundle?) {
        try {
            super.onCreate(savedInstanceState)
            setContentView(R.layout.activity_main)

            titleEditText = findViewById(R.id.title)
            artistEditText = findViewById(R.id.artist)
            albumEditText = findViewById(R.id.album)
            trackEditText = findViewById(R.id.track)

            jacketImageView = findViewById(R.id.jacketImage)


            findViewById<Button>(R.id.selectMP3).setOnClickListener{ view ->
                try {
                    val intent = Intent(Intent.ACTION_OPEN_DOCUMENT)
                    intent.addCategory(Intent.CATEGORY_OPENABLE)
                    intent.type = "audio/mpeg"
                    selectMP3ActivityResultLauncher?.launch(intent)

                } catch (exception: Exception) {
                    Toast.makeText(applicationContext, exception.toString(), Toast.LENGTH_LONG).show()
                    throw exception
                }
            }


            findViewById<Button>(R.id.selectJacketImage).setOnClickListener{ view ->
                try {
                    val intent = Intent(Intent.ACTION_OPEN_DOCUMENT)
                    intent.addCategory(Intent.CATEGORY_OPENABLE)
                    intent.type = "image/*"
                    selectJacketImageActivityResultLauncher?.launch(intent)

                } catch (exception: Exception) {
                    Toast.makeText(applicationContext, exception.toString(), Toast.LENGTH_LONG).show()
                    throw exception
                }
            }


            findViewById<Button>(R.id.makeMP3).setOnClickListener{ view ->
                try {
                    val title = titleEditText?.getText()?.toString() ?: ""
                    val artist = artistEditText?.getText()?.toString() ?: ""
                    val track = trackEditText?.getText()?.toString() ?: ""

                    if (title.isEmpty()) {
                        Toast.makeText(applicationContext, getString(R.string.empty_title_message), Toast.LENGTH_LONG).show()
                        return@setOnClickListener
                    }
                    if (artist.isEmpty()) {
                        Toast.makeText(applicationContext, getString(R.string.empty_artist_message), Toast.LENGTH_LONG).show()
                        return@setOnClickListener
                    }
                    if (track.isEmpty()) {
                        Toast.makeText(applicationContext, getString(R.string.empty_track_message), Toast.LENGTH_LONG).show()
                        return@setOnClickListener
                    }

                    val intent = Intent(Intent.ACTION_CREATE_DOCUMENT)
                    intent.addCategory(Intent.CATEGORY_OPENABLE)
                    intent.type = "audio/mpeg"
                    makeMP3ActivityResultLauncher?.launch(intent)

                } catch (exception: Exception) {
                    Toast.makeText(applicationContext, exception.toString(), Toast.LENGTH_LONG).show()
                    throw exception
                }
            }


        } catch (exception: Exception) {
            Toast.makeText(applicationContext, exception.toString(), Toast.LENGTH_LONG).show()
            throw exception
        }
    }


    override fun onDestroy() {
        try {

            titleEditText = null
            artistEditText = null
            albumEditText = null
            trackEditText = null

            jacketImageView = null

            imageMimetype = null
            imageByteArray = null
            mpegFrameByteArray = null


            selectMP3ActivityResultLauncher?.unregister()
            selectMP3ActivityResultLauncher = null

            selectJacketImageActivityResultLauncher?.unregister()
            selectJacketImageActivityResultLauncher = null

            makeMP3ActivityResultLauncher?.unregister()
            makeMP3ActivityResultLauncher = null


        } catch (exception: Exception) {
            Toast.makeText(applicationContext, exception.toString(), Toast.LENGTH_LONG).show()
            throw exception
        } finally {

            super.onDestroy()
        }
    }
}
