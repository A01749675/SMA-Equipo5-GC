using System.Collections;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using UnityEngine;
using UnityEngine.ProBuilder;
using UnityEngine.UIElements;

public class Movement2 : MonoBehaviour
{
    
    public float x;
    public float z;
    float prevAngle;
    ProBuilderMesh pbMesh;
    List<Vector3> vertices;
    Matrix4x4 carTranslate;
    Vector3 position;
    Matrix4x4 roty;
    Matrix4x4 pneg;
    Matrix4x4 ppos;
    public List<Vector3> positions;
    Vector3 pivot;
    [SerializeField]
    float angle;
    
    Matrix4x4 m;
    float objectiveAngle;
    bool flag;
    float pivConstantX;
    float pivConstantZ;
    Matrix4x4 scale;
    [SerializeField]
    GameObject carPrefab;
    GameObject car;
    [SerializeField]
    Connection con;

    public bool callForNextPos;
    public bool waitingForNextPos;
    bool started;
    bool assignPivot;

    float prev_x;
    float prev_z;

    
    
    


    // Start is called before the first frame update
    void Start()
    {
        positions = new List<Vector3>();
        waitingForNextPos = false;
        // Instancia el prefab del coche
        if (carPrefab != null)
        {
            car = Instantiate(carPrefab);
            car.name = "CarPrueba";
        }
        else
        {
            Debug.LogError("Car prefab is not assigned!");
            return;
        }
        started = false;
        assignPivot = false;
        callForNextPos = true;
        pbMesh = car.GetComponent<ProBuilderMesh>();
        vertices =new List<Vector3>(pbMesh.positions);
        carTranslate = VecOps.TranslateM(new Vector3 (x, 0, z) );
        position = new Vector3 (x, 0, z);
        roty = VecOps.RotateYM(angle);
        Debug.Log(angle);
        Debug.Log(roty);
        scale= VecOps.ScaleM(new Vector3 (1,1,1));
        m =   roty*carTranslate*scale;
        Debug.Log(m);
        pbMesh.positions = VecOps.ApplyTransform(vertices, m).ToArray();
        pbMesh.ToMesh();
        pbMesh.Refresh();
        pivot = new Vector3 (x,0,z);
        ppos = VecOps.TranslateM(pivot);
        pneg = VecOps.TranslateM(-pivot);
        flag = false;
        prev_x = x;
        prev_z = z;
        pivConstantX = 0.0f;
        pivConstantZ = 0.0f;
        
    }

    // Update is called once per frame
    void Update()
    {
        if(!started){
            if(!callForNextPos && !con.addingPos){
                Debug.Log("Receiving positions");
                started = true;
                carTranslate = VecOps.TranslateM(new Vector3 (x, 0, z) );
                position = new Vector3 (x, 0, z);
                roty = VecOps.RotateYM(angle);
                pbMesh.positions = VecOps.ApplyTransform(vertices, m).ToArray();
                pbMesh.ToMesh();
                pbMesh.Refresh();
                prev_x = x;
                prev_z = z;
                Debug.Log("The position is: "+position);
            }
        }
        else{
    //Debug.Log("The position is: "+position);
        if(!callForNextPos && !waitingForNextPos && AproximadamenteIgual(x,position.x,0.1f) && AproximadamenteIgual(z,position.z,0.1f)){
                // Debug.Log("Posiciones: ");
                // foreach(Vector3 pos in positions){
                //     Debug.Log(pos);
                // }
                // Debug.Log("-----------------------------");
                // Debug.Log("En objetivo");
                flag = false;
                callForNextPos = true;
                //con.CallNextPos();
                

            } else{
                objectiveAngle = (360+Mathf.Atan2(z-prev_z, x-prev_x) * Mathf.Rad2Deg)%360;
                

                if(AproximadamenteIgual((360+angle)%360,objectiveAngle,1)){
                    angle = (360+angle)%360;
                    assignPivot = false;
                Debug.Log("The current position is: "+position);
                Debug.Log("The start pos is: "+prev_x+","+prev_z);  
                Debug.Log("The target pos is: "+x+","+z);
                    // Debug.Log("The angle is the same");
                    pivConstantX = 0.0f;
                    pivConstantZ = 0.0f;
                    prevAngle = objectiveAngle;
                    if(AproximadamenteIgual(position.x,x,0.1f)){
                        Debug.Log("The x is the same, moving z");
                        if(position.z < z){
                            move_z(0.01f);
                            //Debug.Log("Arriba");
                        } else{
                            move_z(-0.01f);
                            //Debug.Log("Abajo");
                        }
                    }
                    else{
                        Debug.Log("The z is the same, moving x");
                        if(position.x < x){
                            move_x(0.01f);
                            //Debug.Log("Derecha");
                        } else{
                            move_x(-0.01f);
                            //Debug.Log("Izquierda");
                        }
                    }
                }
                else{
                    assignPivot = true;
                    Debug.Log("The objective angle is: "+objectiveAngle);
                    Debug.Log("The current angle is: "+angle);
                    // if(objectiveAngle>angle){
                    //     Debug.Log("Rotating left");
                    //     rotate_left();
                        
                    // } else{
                    //     Debug.Log("Rotating right");
                    //     rotate_right();

                    // }
                    if(prevAngle == 270 && objectiveAngle == 0){ //South to east
                        Debug.Log("Down to right");
                        rotate_left();
                        pivConstantX = 0.5f;
                        pivConstantZ = -0.0f;
                    } else if(prevAngle == 270 && (objectiveAngle == 180)){ //Down to left
                        rotate_right();
                        pivConstantX = -0.5f;
                        pivConstantZ = 0.0f;
                        Debug.Log("Down to left");

                    } else if(prevAngle == 0 && objectiveAngle == 270){ //Right to down
                        Debug.Log("Right to down");
                        
                        rotate_right();
                        pivConstantX = 0f;
                        pivConstantZ = -0.5f;
                    } 
                    else if(prevAngle == 0 && objectiveAngle == 90){ //Right to up
                        Debug.Log("Right to up");
                        rotate_left();
                        pivConstantX = 0.0f;
                        pivConstantZ = 0.5f;
                    }
                    else if((prevAngle == 180) && objectiveAngle == 270){ //left to down
                        Debug.Log("Left to down");
  
                        rotate_left();
                        
                        pivConstantX = -0.0f;
                        pivConstantZ = -0.5f;
                    
                    } else if((prevAngle == 180) && objectiveAngle == 90){
                        Debug.Log("Left to up");
                        rotate_right();
                        pivConstantX = -0.0f;
                        pivConstantZ = 0.5f;  

                    } else if(prevAngle == 90 && objectiveAngle == 0){ //Up to right
                        Debug.Log("Up to right");
                        rotate_right();
                        pivConstantX = 0.5f;
                        pivConstantZ = 0.0f;
                    } else if(prevAngle == 90 && (objectiveAngle == 180)){ //Up to left
                        rotate_left();
                        Debug.Log("Up to left");
                        pivConstantX = -0.5f;
                        pivConstantZ = 0.0f;
                    }
                    else if(prevAngle == 0 && objectiveAngle == 180){ //Right to left
                        Debug.Log("Right to left");
                        rotate_left();
                        pivConstantX = -0.0f;
                        pivConstantZ = 0.0f;
                    } else if(prevAngle == 180 && objectiveAngle == 0){ //Left to right
                        Debug.Log("Left to right");
                        rotate_right();
                        pivConstantX = 0.0f;
                        pivConstantZ = 0.0f;

                    }
                    else{
                        Debug.Log("No pivot");
                        rotate_left();
                        pivConstantX = 0.0f;
                        pivConstantZ = 0.0f;
                    }
                     pivConstantX = 0.0f;
                     pivConstantZ = 0.0f;
                }
            
            }
            if(assignPivot){
                pivot = new Vector3 (position.x+pivConstantX,position.y,position.z+pivConstantZ);
            }
            else{
                pivot = new Vector3 (position.x,position.y,position.z);
            }
            
            ppos = VecOps.TranslateM(pivot);
            pneg = VecOps.TranslateM(-pivot);
            
            m =  ppos*roty*pneg*carTranslate*scale;

            pbMesh.positions = VecOps.ApplyTransform(vertices, m).ToArray();
            pbMesh.ToMesh();
            pbMesh.Refresh();
        }
    }
    void move_x(float speed)
{
    position.x += speed;
    carTranslate *= VecOps.TranslateM(new Vector3(speed, 0, 0));
}

void move_z(float speed)
{
    position.z += speed;
    carTranslate *= VecOps.TranslateM(new Vector3(0, 0, speed));
}

void rotate_left()
{
    angle++;
    roty *= VecOps.RotateYM(1); // Rotación acumulativa
}

void rotate_right()
{
    angle--;
    roty *= VecOps.RotateYM(-1); // Rotación acumulativa
}

bool AproximadamenteIgual(float valor1, float valor2, float tolerancia = 0.001f)
{
    return Mathf.Abs(valor1 - valor2) < tolerancia;
}

public void setX(float x_n){
    prev_x = x;
    if(x > x_n){
        
        x = x_n+1;
    } else{
        x = x_n;
    }
}

public void setZ(float z_n){
    prev_z = z;
    if(z > z_n){
        z = z_n+1;
    } else{
        z = z_n;
    }
}



}

