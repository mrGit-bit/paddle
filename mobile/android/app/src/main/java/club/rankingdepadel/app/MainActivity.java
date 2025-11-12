package club.rankingdepadel.app;

import android.os.Bundle;
import android.webkit.WebSettings;

import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Normalize text zoom to ignore Android system font scale
        getBridge().getWebView().post(() -> {
            WebSettings settings = getBridge().getWebView().getSettings();
            // Option 1: lock to 100% (identical to Chrome default)
            settings.setTextZoom(100);

            // Option 2 (optional): compensate dynamically if you ever re-enable scaling
            // float scale = getResources().getConfiguration().fontScale;
            // settings.setTextZoom(Math.round(100f / scale));
        });
    }
}
