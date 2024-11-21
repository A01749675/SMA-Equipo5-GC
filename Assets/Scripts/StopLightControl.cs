using System.Collections;
using System.Collections.Generic;
using System.Data.Common;
using System.Diagnostics;
using UnityEngine;

public class StopLightControl : MonoBehaviour
{
    [SerializeField]
    int id;
    public string state;

    GameObject redLight;
    GameObject yellowLight;
    GameObject greenLight;

    // Start is called before the first frame update
    void Start()
    {
        redLight = transform.GetChild(0).gameObject;
        yellowLight = transform.GetChild(1).gameObject;
        greenLight = transform.GetChild(2).gameObject;
    }

    // Update is called once per frame
    void Update()
    {
        switch(state){
            case "Red":
                redLight.SetActive(true);
                yellowLight.SetActive(false);
                greenLight.SetActive(false);
                break;
            case "Yellow":
                redLight.SetActive(false);
                yellowLight.SetActive(true);
                greenLight.SetActive(false);
                break;
            case "Green":
                redLight.SetActive(false);
                yellowLight.SetActive(false);
                greenLight.SetActive(true);
                break;
        }
    }

    public void setState(int id,string newState){
        UnityEngine.Debug.Log("Setting state of "+id+" to "+newState);
        if(id == this.id){
            state = newState;
        }
    }
}
