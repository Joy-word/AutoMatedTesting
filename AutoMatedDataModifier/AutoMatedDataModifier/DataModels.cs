using System;
using System.Collections.Generic;
using System.Text;
using Newtonsoft.Json;

namespace AutoMatedDataModifier {
    public class SessionModel {
        public StepModel Session { get; set; }
    }

    public class StepModel {
        public List<StepActionModel> StepAction { get; set; }
    }

    public class StepActionModel {
        [JsonProperty("@StepNumber")]
        //根据列表来排序，会变动
        public string StepNumber { get; set; }

        public string Location { get; set; }

        public string LocationXY { get; set; }

        public string VisualImagePath { get; set; }

        public ActionModel Action { get; set; } = new ActionModel();

        public string Duration { get; set; }

        public string Broke { get; set; }
        
        public string ReTry { get; set; }

    }

    public class ActionModel {
        [JsonProperty("@type")]
        public string Type { get; set; }

        [JsonProperty("@param")]
        public string Param { get; set; }

        [JsonProperty("#text")]
        public string Value { get; set; }
    }
}
