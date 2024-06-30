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
            public void run() {
                try {
                    URL url = new URL("http://192.168.44.115:1000/api/submit"); // Use your host IP and port
                    HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
                    urlConnection.setRequestMethod("POST");
                    urlConnection.setDoOutput(true);
                    urlConnection.setRequestProperty("Content-Type", "application/json");

                    // Create JSON object to send to the server
                    JSONObject jsonParam = new JSONObject();
                    jsonParam.put("userInput", userInput);

                    // Write the JSON data to the output stream
                    OutputStream os = urlConnection.getOutputStream();
                    os.write(jsonParam.toString().getBytes("UTF-8"));
                    os.close();

                    int responseCode = urlConnection.getResponseCode();
                    if (responseCode == HttpURLConnection.HTTP_OK) { // 200 OK
                        BufferedReader in = new BufferedReader(new InputStreamReader(urlConnection.getInputStream()));
                        String inputLine;
                        StringBuilder response = new StringBuilder();

                        while ((inputLine = in.readLine()) != null) {
                            response.append(inputLine);
                        }
                        in.close();

                        // Update UI with the response on the main thread
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                textViewResponse.setText(response.toString());
                            }
                        });
                    } else {
                        // Handle response code other than 200
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                textViewResponse.setText(message);
                            }
                        });
                    } catch (JSONException e) {
                        e.printStackTrace();
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

/*
* on clicking the button get all the texts
* next:
* HashMp<String,object> data = new hashMap<>();
* data.put("name",name);
* data.put("id",id);
*
* FirebaseDatabase.getInstance().getReference().child("Students").setValue(data).addOnSuccessListener(new On SuccessListener){
*
* }
*
* If we want to connect 2 or more activities with each other, we'll use 'Intent'
*
* Firebase REcycler Adapter
* */