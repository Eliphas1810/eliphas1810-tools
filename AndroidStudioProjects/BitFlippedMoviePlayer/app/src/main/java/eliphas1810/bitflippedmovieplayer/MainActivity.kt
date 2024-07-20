package eliphas1810.bitflippedmovieplayer

import android.content.Intent
import android.net.Uri
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.webkit.ValueCallback
import android.webkit.WebChromeClient
import android.webkit.WebView
import android.widget.*
import androidx.activity.result.ActivityResult
import androidx.activity.result.ActivityResultLauncher
import androidx.activity.result.contract.ActivityResultContracts

class MainActivity : AppCompatActivity() {

    private var valueCallback: ValueCallback<Array<Uri>>? = null

    private var readActivityResultLauncher: ActivityResultLauncher<Intent>? = registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { activityResult: ActivityResult ->

        if (activityResult.resultCode == RESULT_OK) {
            val intent = activityResult.data

            var uriList = mutableListOf<Uri>()

            //2つ以上のファイルが選択された場合
            if (intent?.clipData?.itemCount != null) {

                for (index in 0..(intent?.clipData?.itemCount!! - 1)) {
                    val uri = intent?.clipData?.getItemAt(index)?.uri as Uri

                    uriList.add(uri!!)
                }

                //1つ以下のファイルが選択された場合
            } else {

                if (intent?.data != null) {

                    val uri = intent?.data as Uri

                    uriList.add(uri!!)
                }
            }

            valueCallback?.onReceiveValue(uriList.toTypedArray())
        }

        if (activityResult.resultCode == RESULT_CANCELED) {
            var uriList = mutableListOf<Uri>()
            valueCallback?.onReceiveValue(uriList.toTypedArray())
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        try {
            super.onCreate(savedInstanceState)
            setContentView(R.layout.activity_main)

            val webView = findViewById<ZoomableWebView>(R.id.webView)
            webView?.settings?.javaScriptEnabled = true //JavaScriptを有効化。デフォルトは無効。

            webView?.settings?.allowFileAccess = true //ファイル アクセスを有効化。デフォルトは無効。

            webView?.webChromeClient = object : WebChromeClient() {

                override fun onShowFileChooser(
                    webView: WebView?,
                    filePathCallback: ValueCallback<Array<Uri>>?,
                    fileChooserParams: FileChooserParams?
                ): Boolean {

                    valueCallback = filePathCallback

                    val intent = Intent(Intent.ACTION_OPEN_DOCUMENT)
                    intent.addCategory(Intent.CATEGORY_OPENABLE)
                    intent.type = "*/*"
                    intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true)
                    readActivityResultLauncher?.launch(intent)

                    return true
                }
            }
            webView?.loadUrl("file:///android_asset/BitFlippedMoviePlayer.html")

        } catch (exception: Exception) {
            Toast.makeText(applicationContext, exception.toString(), Toast.LENGTH_LONG).show()
            throw exception
        }
    }

    override fun onDestroy() {
        try {

            valueCallback = null

            readActivityResultLauncher?.unregister()
            readActivityResultLauncher = null

        } catch (exception: Exception) {
            Toast.makeText(applicationContext, exception.toString(), Toast.LENGTH_LONG).show()
            throw exception
        } finally {

            super.onDestroy()
        }
    }
}
