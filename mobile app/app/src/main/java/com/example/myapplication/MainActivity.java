package com.example.myapplication;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;


public class MainActivity extends AppCompatActivity {
    String apiUrl = "192.168.43.226";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        EditText editTextUserInput = findViewById(R.id.editTextInput);
        Button buttonSend = findViewById(R.id.buttonSubmit);
        TextView textViewResponse = findViewById(R.id.textViewResponse);

        buttonSend.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String userInput = editTextUserInput.getText().toString();
                try {
                    sendPostRequest(userInput, textViewResponse);
                } catch (JSONException e) {
                    throw new RuntimeException(e);
                }
            }
        });
    }

    private void sendPostRequest(String userInput, final TextView textViewResponse) throws JSONException {
        OkHttpClient client = new OkHttpClient();

        JSONObject jsonParam = new JSONObject();
        jsonParam.put("message", userInput); // Update the key to "message"

        RequestBody requestBody = RequestBody.create(MediaType.get("application/json; charset=utf-8"), jsonParam.toString());

        Request request = new Request.Builder()
                .url("http://192.168.43.226:1000/api/submit")
                .post(requestBody)
                .build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                e.printStackTrace();
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        textViewResponse.setText("Error: " + e.getMessage());
                    }
                });
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if (response.isSuccessful()) {
                    final String responseBody = response.body().string();
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            textViewResponse.setText(responseBody);
                        }
                    });
                } else {
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            textViewResponse.setText("Error: " + response.code());
                        }
                    });
                }
            }
        });
    }
}