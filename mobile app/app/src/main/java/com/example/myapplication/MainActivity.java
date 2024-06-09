package com.example.myapplication;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;
import org.json.JSONObject;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.io.BufferedReader;
import java.io.InputStreamReader;


public class MainActivity extends AppCompatActivity {

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
                sendPostRequest(userInput, textViewResponse);
            }
        });
    }

    private void sendPostRequest(String userInput, TextView textViewResponse) {
        new Thread(new Runnable() {
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
                                textViewResponse.setText("POST request failed. Response Code: " + responseCode);
                            }
                        });
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                    // Update UI with the exception on the main thread
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            textViewResponse.setText("Exception: " + e.getMessage());
                        }
                    });
                }
            }
        }).start();
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