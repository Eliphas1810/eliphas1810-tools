package eliphas1810.bitflippedimageviewer

import android.content.Context
import android.util.AttributeSet
import android.view.MotionEvent
import android.view.ScaleGestureDetector
import android.webkit.WebView


class ZoomableWebView(
    context: Context,
    attributeSet: AttributeSet?,
    defaultStyleAttribute: Int,
    defaultStyleResourceId: Int
) : WebView(context, attributeSet, defaultStyleAttribute, defaultStyleResourceId), ScaleGestureDetector.OnScaleGestureListener {


    private val scaleGestureDetector = ScaleGestureDetector(context, this)


    private var lastScaleFactor = 1.0f


    constructor(context: Context, attributeSet: AttributeSet?, defaultStyleAttribute: Int) : this(context, attributeSet, defaultStyleAttribute, 0)
    constructor(context: Context, attributeSet: AttributeSet?) : this(context, attributeSet, 0, 0)
    constructor(context: Context) : this(context, null, 0, 0)


    override fun onTouchEvent(motionEvent: MotionEvent?): Boolean {

        scaleGestureDetector.onTouchEvent(motionEvent!!)

        return super.onTouchEvent(motionEvent)
    }


    override fun onScaleBegin(scaleGestureDetector: ScaleGestureDetector): Boolean {
        return true
    }

    override fun onScale(scaleGestureDetector: ScaleGestureDetector): Boolean {

        if ((lastScaleFactor / 0.05f).toInt() == (scaleGestureDetector.scaleFactor / 0.05f).toInt()) {
            return true
        }

        lastScaleFactor = scaleGestureDetector.scaleFactor

        //ピンチアウトの場合
        //
        //拡大の場合
        //
        if (1.0f < scaleGestureDetector.scaleFactor) {

            zoomIn()

        //ピンチインの場合
        //
        //縮小の場合
        //
        } else {

            zoomOut()
        }

        return true
    }

    override fun onScaleEnd(scaleGestureDetector: ScaleGestureDetector) {
    }
}
