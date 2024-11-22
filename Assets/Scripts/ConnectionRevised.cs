using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.Networking;

public class ConnectionRevised : MonoBehaviour
{
    List<List<Vector3>> positions;
    List<Stoplight> stoplights;
    List<Car> carData;
    AllData allData;

    public bool addingPos;
    int llamadas;

    [SerializeField]
    Vehicles vehicles;

    float time;
    float timeToRequest = 1.0f;

    IEnumerator RequestAllData()
    {
        WWWForm form = new WWWForm();
        string url = "http://localhost:8000/allData";
        using (UnityWebRequest www = UnityWebRequest.Post(url, form))
        {
            www.downloadHandler = new DownloadHandlerBuffer();
            www.SetRequestHeader("Content-Type", "application/json");
            yield return www.SendWebRequest();
            if (www.result == UnityWebRequest.Result.ConnectionError)
            {
                Debug.Log(www.error);
            }
            else
            {
                string response = www.downloadHandler.text;
                Debug.Log("Response: " + response);
                allData = AllData.CreateFromJSON(response);
                Debug.Log("AllData deserialized");
                carData = allData.cars.cars;
                Stoplights stoplights = allData.stoplights;
                Debug.Log("Cars: " + carData.Count);
                Debug.Log("Stoplights: " + stoplights.stoplights.Count);
                if (vehicles.vehicles.Count == carData.Count&& vehicles.vehicles.Count > 0)
                {
                    Debug.Log("Adding positions");
                    for (int i = 0; i < vehicles.vehicles.Count; i++)
                    {
                        Debug.Log("Car data: " + carData[i].x + ", " + carData[i].z);
                        vehicles.vehicles[i].AddPositions(new Vector3(carData[i].x, 0, carData[i].z));
                    }
                }
                else
                {
                    Debug.LogWarning("Mismatch in number of cars and vehicles.");
                }
            }
        }
    }

 IEnumerator RequestCarPositions()
    {
        WWWForm form = new WWWForm();
        string url = "http://localhost:8000/carData";
        using (UnityWebRequest www = UnityWebRequest.Post(url,form))
        {
            www.downloadHandler = new DownloadHandlerBuffer();
            www.SetRequestHeader("Content-Type","application/json");
            yield return www.SendWebRequest();
            if(www.result == UnityWebRequest.Result.ConnectionError){
                Debug.Log(www.error);
            }
            else{
                string response = www.downloadHandler.text;
                carData = Cars.CreateFromJSON(response).cars;

                if (vehicles.vehicles.Count == carData.Count&& vehicles.vehicles.Count > 0)
                {

                    for (int i = 0; i < vehicles.vehicles.Count; i++)
                    {
                        vehicles.vehicles[i].AddPositions(new Vector3(carData[i].x, 0, carData[i].z));
                    }
                }
                else
                {
                    Debug.LogWarning("Mismatch in number of cars and vehicles.");
                }

                
            }
        }
        llamadas +=1;
        //Debug.Log(llamadas);
    }

    // Start is called before the first frame update
    void Start()
    {
        time = 5.0f;
        bool start = false;
        while (!start)
        {
            Debug.Log("Waiting for data");
            StartCoroutine(RequestCarPositions());
            foreach (Vehicle vehicle in vehicles.vehicles)
            {
                start = vehicle.MetStartingConditions();
            }
        }
    }

    // Update is called once per frame
    void FixedUpdate()
    {
        time -= Time.deltaTime;
        if (time <= 0)
        {
            time = 1f;
            StartCoroutine(RequestCarPositions());
        }
    }
}