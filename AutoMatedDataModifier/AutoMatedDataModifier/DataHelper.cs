using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Text;
using System.Xml;

namespace AutoMatedDataModifier {
    public static class DataHelper {
        public static string XmlToJson(string xmlPath) {
            XmlDocument doc = new XmlDocument();
            doc.Load(xmlPath);
            return JsonConvert.SerializeXmlNode(doc);
        }
        public static string XmlToJson(XmlDocument doc) {
            return JsonConvert.SerializeXmlNode(doc);
        }

        public static XmlDocument JsonToXml(string json) {
            return JsonConvert.DeserializeXmlNode(json);
        }
    }
}
