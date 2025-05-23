using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.ProBuilder;
public class Vehicle : MonoBehaviour
{
    

    int vehicleIndex;

    int windowSize;

    int id;

    ProBuilderMesh pbMesh;
    List<Vector3> vertices;
    Matrix4x4 carTranslate;
    Vector3 position;
    Matrix4x4 roty;
    Matrix4x4 pneg;
    Matrix4x4 ppos;

    GameObject carPrefab;

    bool first = false;

    public List<Vector3> positions = new List<Vector3>();

    
    // Start is called before the first frame update

    public void SetId(int id){
        this.id = id;
    }
    
    public void AddPositions(Vector3 position){
        positions.Add(position);
    }
    public void SetPrefab(GameObject carPrefab){
        this.carPrefab = carPrefab;
    }

    public bool MetStartingConditions(){
        return positions.Count >= windowSize;
    }

    void Start()
    {
        windowSize = 4;
        positions = new List<Vector3>();   
    }
    public List<Vector3> Window(){
        if(positions.Count < 4){
            return positions;
        }
        List<Vector3> result = new List<Vector3>();
        int start = positions.Count-4;
        for(int i = 0; i < 4; i++){
            result.Add(positions[start+i]);
        }

        return result;
    }

    // Update is called once per frame
    void Update()
    {
        // if(carPrefab && !first){
        //     if(positions.Count >= windowSize){
        //         Instantiate(carPrefab,positions[positions.Count-1],Quaternion.identity);
        //         first = true;
        //     }
        // }   
    }
}
