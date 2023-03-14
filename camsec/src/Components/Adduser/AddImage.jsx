import React,{useState} from "react";
import Username from "./Username";
import Userid from "./Userid";
import {AiOutlineDownload,MdOutlineDelete,MdMessage,AiOutlineCloudDownload,BsCloudArrowUp} from "react-icons/all"
import Authority from "../Camsetting/Authority/Authority1";
import { MDBCard, MDBCardBody, MDBCardTitle } from "mdb-react-ui-kit";
const AddImage = () => {
    const [image, setImage] = useState({
        bytes: "",
        file: "/noimage.jpg",
      });
      const [f1,setF1]=useState(false)
      const handle=(event)=>{
        setImage({
            bytes: event.target.files[0],
            file: URL.createObjectURL(event.target.files[0]),
             })
             setF1(true)
      }
      localStorage.setItem('o',image.file)
      const handle1=()=>{
          setImage({
            bytes: "",
            file: "/noimage.jpg",
          })
          setF1(false)
      }
  return (
    <div className="adduser">
      <div className="home">
        <div className="head">
          <div className="heading">
            <div className="head1">HEALTHCARE SEC</div>
            <div className="head2">CAMSEC.AI</div>
          </div>
        </div>
        </div>
        <hr id="hr"/>
        <div className="adduser-panel1">
            <div className="adduser-fields1">
                {f1===false?<div>
                <div className="" style={{width:'100%'}}>
                <div className="">
                 <h2 style={{color:'white',marginTop:'2%',display:'flex',justifyContent:'center',alignItems:'center'}}><b>Upload Your Image</b></h2>
                 <b style={{color:'white',display:'flex',fontSize:'15px',justifyContent:'center',alignItems:'center'}}>PNG AND JPG files are allowed</b>
                 <div style={{marginTop:'3%',color:'white',display:'flex',justifyContent:'center',alignItems:'center'}}>
                <BsCloudArrowUp style={{color:'white',fontSize:'115px'}}/>
                </div>
                <div style={{marginTop:'4%',color:'white',display:'flex',justifyContent:'center',alignItems:'center'}}>
                <div>
                    <input onChange={(event) =>handle(event)
                     } type="file" id="actual-btn" hidden />
                    <label id="choose"style={{textDecoration:'underline',fontSize:'19px',cursor:'pointer',textDecorationStyle:'solid'}}  for="actual-btn">Drag And drop or browes to choose a file</label>
                </div>
               </div>
               </div>
                </div>
                </div>:
                <div style={{display:'flex',marginTop:'10vh',justifyContent:'center',alignItems:'center'}}><img style={{height:'33vh',width:'33vh'}} src={image.file}></img>
                </div>} 
                <div className=""style={{marginLeft:'4%',display:'flex',marginTop:'6%',justifyContent:'center',alignItems:'center'}}>
                    <button onClick={()=>window.location.assign("addimage")} style={{background:'white',color:'black',height:'49px',marginTop:'0px',width:'12%'
                    ,borderRadius:'9px',fontSize:''}}><AiOutlineDownload style={{marginRight:'6px'}} />Save</button>
                   <button onClick={()=>handle1()} style={{background:'white',color:'black',height
                   :'49px',marginLeft:'2%',marginTop:'0px',width:'18%',borderRadius:'9px',fontSize:'19px',marginRight:'3%'}}><MdOutlineDelete style={{marginRight:'10px'}} />Discard</button>
                </div>
                </div> 
        </div>    
    </div>
  );
};

export default AddImage;
