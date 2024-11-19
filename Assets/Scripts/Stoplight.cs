using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class Stoplight 
{
    public int id;
    public string state;

    public static Stoplight CreateFromJSON(string jsonString)
    {
        return JsonUtility.FromJson<Stoplight>(jsonString);
    }
}
