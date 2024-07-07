package com.example.myapplication;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONException;
import org.json.JSONObject;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

import java.io.IOException;

public class MainActivity extends AppCompatActivity {
    String apiUrl = "http://192.168.1.15:8000/api/text_message";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        EditText editTextUserInput = findViewById(R.id.editTextInput);
        Button buttonSend = findViewById(R.id.buttonSubmit);
        TextView textViewResponse = findViewById(R.id.chat_container);

        buttonSend.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String userInput = editTextUserInput.getText().toString();
                try {
                    sendPostRequest(userInput, textViewResponse);
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        });
    }

    private void sendPostRequest(String userInput, final TextView textViewResponse) throws JSONException {
        OkHttpClient client = new OkHttpClient();

        JSONObject jsonParam = new JSONObject();
        jsonParam.put("message", userInput);

        RequestBody requestBody = RequestBody.create(MediaType.get("application/json; charset=utf-8"), jsonParam.toString());

        Request request = new Request.Builder()
                .url(apiUrl)
                .post(requestBody)
                .build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        textViewResponse.setText("Request Failed: " + e.getMessage());
                    }
                });
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                if (response.isSuccessful()) {
                    try {
                        final JSONObject responseData = new JSONObject(response.body().string());

                        // Extract the "message_returned" value
                        String message = responseData.getString("message_returned");
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                textViewResponse.setText(message);
                            }
                        });
                    }
                    catch (JSONException e) {
                        e.printStackTrace();
                        // Handle JSON parsing error (optional: display an error message)
                    }
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