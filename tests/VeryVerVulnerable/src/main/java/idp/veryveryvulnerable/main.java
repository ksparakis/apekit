package idp.veryveryvulnerable;

import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothHeadset;
import android.content.Intent;
import android.net.Uri;
import android.os.IBinder;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;

import java.io.File;
import java.security.KeyStore;
import java.util.HashMap;

import android.os.IBinder;

import android.os.Binder;

import com.google.android.gms.appindexing.Action;
import com.google.android.gms.appindexing.AppIndex;
import com.google.android.gms.common.api.GoogleApiClient;

public class main extends AppCompatActivity {

    public static final String MESSAGE_SENT_ACTION =
            "com.android.mms.transaction.MESSAGE_SENT";

    // not using HTTPS
    public static final String URL = "http://api.twitter.com/1/";

    public static final String ACCESS_TO = "/dev/msm_acdb";

    private final IBinder mBinder = new Binder();

    private GoogleApiClient client;

    IWapPushManager getInterface() {
        IWapPushManager mWapPush = new IWapPushManager();
        if (mWapPush != null) return mWapPush;
        Intent startIntent = new Intent();

        return mWapPush;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        IWapPushManager wapPushMan = new IWapPushManager();

        int procRet = wapPushMan.processMessage();

        kgsl_ioctl();

        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        client = new GoogleApiClient.Builder(this).addApi(AppIndex.API).build();
    }

    private void kgsl_ioctl() {
        // this represents the kgsl call that opens one up to a DOS attack
    }

    public IBinder onBind(Intent intent) {
        return mBinder;
    }

    public boolean createIncomingConnect(BluetoothDevice device) {
        BluetoothHeadsetService x = new BluetoothHeadsetService();
        synchronized (x) {
            return true;
        }
    }

    @Override
    public void onStart() {
        super.onStart();

        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        client.connect();
        Action viewAction = Action.newAction(
                Action.TYPE_VIEW, // TODO: choose an action type.
                "main Page", // TODO: Define a title for the content shown.
                // TODO: If you have web page content that matches this app activity's content,
                // make sure this auto-generated web page URL is correct.
                // Otherwise, set the URL to null.
                Uri.parse("http://host/path"),
                // TODO: Make sure this auto-generated app deep link URI is correct.
                Uri.parse("android-app://idp.veryveryvulnerable/http/host/path")
        );
        AppIndex.AppIndexApi.start(client, viewAction);

        FrameworkListener a = new FrameworkListener();
        a.dispatchCommand();

        idp.veryveryvulnerable.KeyStore b = new idp.veryveryvulnerable.KeyStore();
        b.encode_key();

        createChain();
        findCert();

    }

    private void createChain() {
        return;
    }

    private void findCert(){
        return;
    }

    @Override
    public void onStop() {
        super.onStop();

        // ATTENTION: This was auto-generated to implement the App Indexing API.
        // See https://g.co/AppIndexing/AndroidStudio for more information.
        Action viewAction = Action.newAction(
                Action.TYPE_VIEW, // TODO: choose an action type.
                "main Page", // TODO: Define a title for the content shown.
                // TODO: If you have web page content that matches this app activity's content,
                // make sure this auto-generated web page URL is correct.
                // Otherwise, set the URL to null.
                Uri.parse("http://host/path"),
                // TODO: Make sure this auto-generated app deep link URI is correct.
                Uri.parse("android-app://idp.veryveryvulnerable/http/host/path")
        );
        AppIndex.AppIndexApi.end(client, viewAction);
        client.disconnect();
    }
}
