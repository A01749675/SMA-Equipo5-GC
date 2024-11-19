using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
public class Connection : MonoBehaviour
{

    List<List<Vector3>> positions;
    List<Stoplight> stoplights;
    List<Car> carData;


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

                foreach(Car car in carData){
                    Debug.Log(car.x+ " "+car.z);
                }
            }
        }
    }

    IEnumerator RequestStoplightData()
    {
        WWWForm form = new WWWForm();
        string url = "http://localhost:8000/stoplightData";
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
                stoplights = Stoplights.CreateFromJSON(response).stoplights;
                foreach(Stoplight stoplight in stoplights){
                    Debug.Log(stoplight.id+ " "+stoplight.state);
                }
            }
        }
    }



    // Start is called before the first frame update
    void Start()
    {
        StartCoroutine(RequestCarPositions());
        StartCoroutine(RequestStoplightData());
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
