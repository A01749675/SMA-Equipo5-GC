using System.Collections;
using System.Collections.Generic;
using UnityEngine;
[System.Serializable]
public class Car 
{
    public int id;
    public int x;
    public int z;

    public static Car CreateFromJSON(string jsonString)
    {
        return JsonUtility.FromJson<Car>(jsonString);
    }
  
}
