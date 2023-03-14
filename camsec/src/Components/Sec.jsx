import React from "react";
import { Link } from "react-router-dom";
const Sec =() =>{
    return(
        <div>
            <div className="sec">       
             <div className="sec1">
             <Link to='Eventoccur1'>
                <div className="count co">45
                 </div>
                 <div className="mask">Mask</div>
                 <div className="mask1000">Alert</div>
                 {/* <b className="face">FaceMetr</b> */}
                 </Link> 
                </div>         
              <div className="sec2">
                <div className="count co">45
                 </div>  
                 <div className="mask">Attendance</div>
                 <div className="mask1000">Monitoring</div>     
                 {/* <div className="mask1">Attendence Monitoring</div>         */}
                 {/* <b className="ric">ic Sec</b> */}
                </div>
        </div>
        </div>
    )
}

export default Sec;