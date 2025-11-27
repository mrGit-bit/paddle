// path: mobile/android/app/src/main/java/club/rankingdepadel/app/MainActivity.java

package club.rankingdepadel.app;

import androidx.core.view.WindowCompat;
import android.os.Bundle;
import android.webkit.WebSettings;
import android.view.WindowManager;

import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        // ⛔ Disable forced edge-to-edge on Android 15 (API 35)
        // This prevents the navbar from overlapping your web content.
        WindowCompat.setDecorFitsSystemWindows(getWindow(), true);

        // Normalize text zoom to ignore Android system font scale
        getBridge().getWebView().post(() -> {
            WebSettings settings = getBridge().getWebView().getSettings();
            // Lock to 100% (identical to Chrome default)
            settings.setTextZoom(100);
        });
    }
}
