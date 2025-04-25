package eliphas1810.bitflipper

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material3.Text
import androidx.compose.material3.Button
import androidx.compose.material3.Surface
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.ui.Alignment
import android.widget.Toast
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts

import eliphas1810.bitflipper.ui.theme.BitFlipperTheme

import androidx.compose.runtime.Composable
import androidx.compose.ui.tooling.preview.Preview

import kotlin.experimental.inv


class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            BitFlipperTheme {
                BuildView()
            }
        }
    }
}


@Composable
fun BuildView() {
    val context = LocalContext.current

    val readLabel = context.getString(R.string.read)
    val saveLabel = context.getString(R.string.save)
    val savedMessage = context.getString(R.string.saved)
    val license = context.getString(R.string.license)

    var byteArray: ByteArray = ByteArray(0)

    var fileUriString by rememberSaveable { mutableStateOf("") }

    val readRememberLauncherForActivityResult = rememberLauncherForActivityResult(ActivityResultContracts.GetContent()) { uri ->

        if (uri == null) {
            return@rememberLauncherForActivityResult
        }

        fileUriString = uri?.toString() ?: ""

        context.contentResolver.openInputStream(uri!!).use {
            byteArray = it?.readBytes() ?: ByteArray(0)
        }

        //ビット反転
        for (index in byteArray.indices) {
            byteArray[index] = byteArray[index].inv()
        }
    }


    val saveRememberLauncherForActivityResult = rememberLauncherForActivityResult(ActivityResultContracts.CreateDocument()) { uri ->

        if (uri == null) {
            return@rememberLauncherForActivityResult
        }

        //contentResolver.openOutputStream()で"wt"モードを指定しないと、書き込み前のバイト サイズが大きい場合、書き込み前のバイトの先頭の一部を置換するような形に成ってしまいます。
        context.contentResolver.openOutputStream(uri!!, "wt").use {
            it?.write(byteArray)
        }

        Toast.makeText(context.applicationContext, savedMessage, Toast.LENGTH_LONG).show()
    }


    Surface(
        modifier = Modifier.fillMaxSize()
    ) {
        Column (
            modifier = Modifier.verticalScroll(rememberScrollState()).padding(5.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Spacer(Modifier.size(20.dp))
            Row {
                Button(
                    onClick = {

                        readRememberLauncherForActivityResult.launch("*/*")
                    }
                ) {
                    Text(readLabel)
                }
            }
            Row {
                Text(text = fileUriString)
            }
            Row {
                Button(
                    onClick = {

                        saveRememberLauncherForActivityResult.launch("")
                    }
                ) {
                    Text(saveLabel)
                }
            }
            Spacer(Modifier.size(10.dp))
            Text(text = license)
        }
    }
}


@Preview(showBackground = true)
@Composable
fun PreviewBuildView() {
    BitFlipperTheme {
        BuildView()
    }
}
