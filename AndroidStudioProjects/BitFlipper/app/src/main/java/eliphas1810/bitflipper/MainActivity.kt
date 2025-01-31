package eliphas1810.bitflipper

import android.content.Intent
import android.net.Uri
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.*
import androidx.activity.result.ActivityResult
import androidx.activity.result.ActivityResultLauncher
import androidx.activity.result.contract.ActivityResultContracts.StartActivityForResult
import androidx.documentfile.provider.DocumentFile
import kotlin.experimental.inv


class MainActivity : AppCompatActivity() {


    var fileNameTextView: TextView? = null


    private var byteArray: ByteArray = ByteArray(0)


    private var readActivityResultLauncher: ActivityResultLauncher<Intent>? = registerForActivityResult(StartActivityForResult()) { activityResult: ActivityResult ->

        if (activityResult.resultCode == RESULT_OK) {
            val intent = activityResult.data

            val uri: Uri? = intent?.data

            val documentFile = DocumentFile.fromSingleUri(applicationContext, uri!!)

            fileNameTextView?.text = documentFile?.name

            contentResolver.openInputStream(uri!!).use {
                byteArray = it?.readBytes() ?: ByteArray(0)
            }

            //ビット反転
            for (index in byteArray.indices) {
                byteArray[index] = byteArray[index].inv()
            }
        }
    }


    private var saveActivityResultLauncher: ActivityResultLauncher<Intent>? = registerForActivityResult(StartActivityForResult()) { activityResult: ActivityResult ->

        if (activityResult.resultCode == RESULT_OK) {
            val intent = activityResult.data

            val uri: Uri? = intent?.data

            //contentResolver.openOutputStream()で"wt"モードを指定しないと、書き込み前のバイト サイズが大きい場合、書き込み前のバイトの先頭の一部を置換するような形に成ってしまいます。
            contentResolver.openOutputStream(uri!!, "wt").use {
                it?.write(byteArray)
            }
        }
    }


    override fun onCreate(savedInstanceState: Bundle?) {
        try {
            super.onCreate(savedInstanceState)
            setContentView(R.layout.activity_main)


            fileNameTextView = findViewById(R.id.fileName)


            findViewById<Button>(R.id.read).setOnClickListener{ view ->
                try {
                    val intent = Intent(Intent.ACTION_OPEN_DOCUMENT)
                    intent.addCategory(Intent.CATEGORY_OPENABLE)
                    intent.type = "*/*"
                    readActivityResultLauncher?.launch(intent)

                } catch (exception: Exception) {
                    Toast.makeText(applicationContext, exception.toString(), Toast.LENGTH_LONG).show()
                    throw exception
                }
            }


            findViewById<Button>(R.id.save).setOnClickListener{ view ->
                try {
                    val intent = Intent(Intent.ACTION_CREATE_DOCUMENT)
                    intent.addCategory(Intent.CATEGORY_OPENABLE)
                    intent.type = "*/*"
                    saveActivityResultLauncher?.launch(intent)

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


            fileNameTextView = null


            byteArray = ByteArray(0)


            readActivityResultLauncher?.unregister()
            readActivityResultLauncher = null


            saveActivityResultLauncher?.unregister()
            saveActivityResultLauncher = null


        } catch (exception: Exception) {
            Toast.makeText(applicationContext, exception.toString(), Toast.LENGTH_LONG).show()
            throw exception
        } finally {

            super.onDestroy()
        }
    }
}
