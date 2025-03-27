package eliphas1810.jasimplemp3idv2tageditor

import android.content.Context
import android.graphics.Matrix
import android.util.AttributeSet
import android.view.GestureDetector
import android.view.MotionEvent
import android.view.ScaleGestureDetector
import androidx.appcompat.widget.AppCompatImageView

class ZoomableImageView(context: Context, attributeSet: AttributeSet?, defaultStyleAttribute: Int) : AppCompatImageView(context, attributeSet, defaultStyleAttribute), ScaleGestureDetector.OnScaleGestureListener {

    constructor(context: Context, attributeSet: AttributeSet?) : this(context, attributeSet, 0)
    constructor(context: Context) : this(context, null, 0)

    val scaleGestureDetector = ScaleGestureDetector(context, this)

    val simpleOnGestureListener = object : GestureDetector.SimpleOnGestureListener() {

        override fun onScroll(
            e1: MotionEvent?,
            motionEvent1: MotionEvent,
            distanceX: Float,
            distanceY: Float
        ): Boolean {

            val imageViewWidth = width
            val imageViewHeight = height

            val imageMatrixValues = FloatArray(9)
            imageMatrix.getValues(imageMatrixValues)

            val imageWidth = imageViewWidth * imageMatrixValues[Matrix.MSCALE_X]
            val imageHeight = imageViewHeight * imageMatrixValues[Matrix.MSCALE_Y]

            var x = 0.0f
            var y = 0.0f

            //縮小中の画像が画像ビューよりも小さい場合
            //
            //画像が画像ビューよりも小さい場合
            //
            if (imageWidth < imageViewWidth) {
                //画像を動かさない
                //x = 0.0f

                //拡大中の画像が画像ビューよりも大きい場合
                //
                //画像が画像ビューよりも大きい場合

                //画像の左端が画像ビューと画面よりも右に離れていて、更に指を左へ動かして、画像を逆方向の更に右へ動かそうとした場合
            } else if (distanceX < 0.0f && 0.0f < imageMatrixValues[Matrix.MTRANS_X]) {
                //画像を元にゼロに戻す
                x = 0.0f - imageMatrixValues[Matrix.MTRANS_X]

                //画像の右端が画像ビューと画面よりも左に離れていて、更に指を右へ動かして、画像を逆方向の更に左へ動かそうとした場合
            } else if ((imageWidth + imageMatrixValues[Matrix.MTRANS_X]) < imageViewWidth && 0.0f < distanceX) {

                //画像の右端を画像ビューと画面の右端に戻す
                //
                //画像の右端と、画像ビューと画面の右端の差分だけ戻す
                //
                x = imageViewWidth - (imageWidth + imageMatrixValues[Matrix.MTRANS_X])

                //その他の場合
            } else {
                //指で動かした分だけ逆方向へ動かす
                x = 0.0f - distanceX
            }

            //縮小中の画像が画像ビューよりも小さい場合
            //
            //画像が画像ビューよりも小さい場合
            //
            if (imageHeight < imageViewHeight) {
                //画像を動かさない
                //y = 0.0f

                //拡大中の画像が画像ビューよりも大きい場合
                //
                //画像が画像ビューよりも大きい場合

                //画像の上端が画像ビューと画面よりも下に離れていて、更に指を上へ動かして、画像を逆方向の更に下へ動かそうとした場合
            } else if (distanceY < 0.0f && 0.0f < imageMatrixValues[Matrix.MTRANS_Y]) {

                //画像を元にゼロに戻す
                y = 0.0f - imageMatrixValues[Matrix.MTRANS_Y]

                //画像の下端が画像ビューと画面よりも上に離れていて、更に指を下へ動かして、画像を逆方向の更に上へ動かそうとした場合
            } else if ((imageHeight + imageMatrixValues[Matrix.MTRANS_Y]) < imageViewHeight && 0.0f < distanceY) {

                //画像の下端を画像ビューと画面の下端に戻す
                //
                //画像の下端と、画像ビューと画面の下端の差分だけ戻す
                //
                y = imageViewHeight - (imageHeight + imageMatrixValues[Matrix.MTRANS_Y])

                //その他の場合
            } else {
                //指で動かした分だけ逆方向へ動かす
                y = 0.0f - distanceY
            }

            //画像を移動
            imageMatrix.postTranslate(x, y)

            //画像ビューの枠内の画像を再描画
            invalidate()

            return super.onScroll(e1, motionEvent1, distanceX, distanceY)
        }
    }

    val gestureDetector = GestureDetector(context, simpleOnGestureListener)

    val minScaleFactor = 0.5f

    override fun onTouchEvent(motionEvent: MotionEvent?): Boolean {
        gestureDetector.onTouchEvent(motionEvent!!)
        scaleGestureDetector.onTouchEvent(motionEvent!!)
        return true
    }

    override fun onScaleBegin(scaleGestureDetector: ScaleGestureDetector): Boolean {
        return true
    }

    override fun onScale(scaleGestureDetector: ScaleGestureDetector): Boolean {

        var scaleFactor = scaleGestureDetector.scaleFactor

        if (scaleFactor == 1.0f) {
            return true
        }

        if (scaleFactor < minScaleFactor) {
            scaleFactor = minScaleFactor
        }

        super.setScaleType(ScaleType.MATRIX)
        val imageMatrix = super.getImageMatrix()
        imageMatrix.postScale(scaleFactor, scaleFactor)
        super.setImageMatrix(imageMatrix)

        val layoutParams = super.getLayoutParams()
        layoutParams.width = (super.getWidth() * scaleFactor).toInt()
        layoutParams.height = (super.getHeight() * scaleFactor).toInt()
        super.setLayoutParams(layoutParams)

        return true
    }

    override fun onScaleEnd(scaleGestureDetector: ScaleGestureDetector) {
    }
}
