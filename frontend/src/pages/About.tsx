import { useContentReady } from "../composables/usePageTransition";
import logoSvg from "../assets/logo.svg";
import lastroImg from "../assets/images/lastro.jpeg";
import curaImg from "../assets/images/cura.jpg";
import logo_rp from "../assets/logo_rp.png";
import logo_uc from "../assets/logo_uc.png";

const About: React.FC = () => {
  useContentReady(true);

  return (
    <div className="grid-setup !pt-[var(--menu-height)] overflow-x-clip">
      <div className="grid grid-cols-1 md:grid-cols-[1fr_2fr] gap-0 md:gap-12 lg:gap-16">
        <div
          className="sticky order-2 md:order-1 flex flex-col self-start md:h-[calc(100vh-var(--menu-height)*2-1.5rem)]"
          style={{
            top: "var(--menu-height)",
          }}
        >
          <div className="bg-color-bg z-20 pt-px pb-3">
            <h2 className="text-title-2 my-3">Links Externos</h2>
            <span className="block h-px w-full bg-color-1 opacity-50" />
          </div>
          <div className="flex flex-col justify-between flex-1 min-h-0">
            <div className="flex flex-col gap-2 md:gap-0">
              <a
                className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-250"
                href="https://amusicaportuguesaagostardelapropria.org/"
                target="_blank"
              >
                Website
              </a>
              <a
                className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-250"
                href="https://vimeo.com/mpagdp"
                target="_blank"
              >
                Vimeo
              </a>
              <a
                className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-250"
                href="https://www.facebook.com/amusicaportuguesaagostardelapropria"
                target="_blank"
              >
                Facebook
              </a>
              <a
                className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-250"
                href="https://www.instagram.com/mpagdp/"
                target="_blank"
              >
                Instagram
              </a>
              <a
                className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-250"
                href="https://www.tiktok.com/@mpagdp.official"
                target="_blank"
              >
                TikTok
              </a>
              <a
                className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-250"
                href="https://linktr.ee/mpagdp"
                target="_blank"
              >
                Mais
              </a>
            </div>
            <div className="mt-16 flex flex-col gap-2 md:gap-0">
               <a
              className="flex items-center gap-3 pb-4 "
              href="https://amusicaportuguesaagostardelapropria.org/"
              target="_blank"
                >
              <img src={logoSvg} alt="Logo" className="w-10 h-10 mb-4" />
              </a>
              <p className="text-body-2 text-color-2">Financiado por</p>
              <div className="flex items-center gap-3 pb-4">
                
              
              <img src={logo_uc} alt="Logo" className="w-10 h-10 object-contain" />
              <img src={logo_rp} alt="Logo" className="w-10 h-10 object-contain" />
              

                
                </div>
             
              <p className="text-body-2 text-color-2">
                2026. Todos os direitos reservados.
              </p>

              <p className="text-body-2 text-color-2">
                Com ❤︎ por{" "}
                <a
                  className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-250 underline"
                  href="https://thomasfresco.pt/"
                  target="_blank"
                >
                  Thomas Fresco
                </a>{" "}
                e{" "}
                <a
                  className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-250 underline"
                  href="https://fabiogouveia.pt/"
                  target="_blank"
                >
                  Fábio Gouveia
                </a>
                .
              </p>
            </div>
          </div>
        </div>
        <div className="flex flex-col order-1 md:order-2">
          <div className="mb-12">
            <div
              className="sticky bg-color-bg z-10 pt-px pb-3"
              style={{ top: "var(--menu-height)" }}
            >
              <h2 className="text-title-2 my-3">Sobre Lastro</h2>
              <span className="block h-px w-full bg-color-1 opacity-50" />
            </div>
            <div className="w-full mb-4 aspect-[5/2] overflow-hidden rounded-lg">
              <img
                src={lastroImg}
                alt="Lastro"
                className="w-full h-full object-cover grayscale"
                style={{ objectPosition: "50% 0%" }}
              />
            </div>
            <div className="flex flex-col gap-3 pr-8">
              <p>
                Lastro propõe uma nova forma de explorar música, tradição oral,
                memória coletiva e património humano.
              </p>
              <p>
                A plataforma permite uma exploração interativa do acervo d'A
                Música Portuguesa A Gostar Dela Própria. O resultado de anos de
                gravações de música, tradição oral, gastronomia e memória
                colectiva alimenta um motor de busca capaz de compreender
                linguagem natural, ajudando a encontrar não só o que procuramos,
                mas também o que pode surgir aleatoriamente durante a procura,
                podendo às vezes a experiência ser muito normativa ou bastante
                disruptiva.
              </p>
              <p>
                O mais importante é que finalmente o projeto tem um lugar onde
                de facto se podem encontrar todos os vídeos que gravou e os que
                continua a gravar.
              </p>
            </div>
          </div>
          <div className="mb-12">
            <div
              className="sticky bg-color-bg z-10 pt-px pb-3"
              style={{ top: "var(--menu-height)" }}
            >
              <h2 className="text-title-2 my-3">
                Sobre A Música Portuguesa a Gostar Dela Própria
              </h2>
              <span className="block h-px w-full bg-color-1 opacity-50" />
            </div>
            <div className="w-full mb-4 aspect-[5/2] overflow-hidden rounded-lg">
              <img
                src={curaImg}
                alt="A Música Portuguesa a Gostar Dela Própria"
                className="w-full h-full object-cover grayscale"
                style={{ objectPosition: "50% 80%" }}
              />
            </div>
            <div className="flex flex-col gap-3 pr-8">
              <p>
                A música Portuguesa a gostar dela própria é fundada em 2011, por
                Tiago Pereira e Joana Barra Vaz, com o intuito de fazer
                convergir no mesmo lugar a diversidade da música portuguesa,
                gravando vídeos de músicos em lugares não convencionais por todo
                o país. Em Março do mesmo ano é fundada a Associação Cultural
                com o mesmo nome. O projecto tem estado sempre em transformação,
                contando com dezenas de colaboradores ao longo dos tempos.
              </p>
              <p>
                O seu principal objectivo é o registo de práticas musicais,
                tradição oral e memória colectiva da cultura popular portuguesa,
                acompanhando as transformações de uma cultura sempre em
                constante movimento e mudança, não apenas como espectador mas de
                uma forma mais interventiva, através da produção de
                Documentários para televisão, programas de rádio, programação
                cultural e intervenção criativa em diversos territórios,
                mapeando práticas, fomentando oficinas de instrumentos
                tradicionais e criando pontes entre gerações, com uma
                participação activa em escolas e com jovens. A partir de 2020, a
                associação muda-se para Serpins, Lousã onde cria um espaço
                aberto ao público: “Cura” onde programa Oficinas e espectáculos,
                promove a diversidade e cria um coro para que as canções que vai
                gravando pelo país se mantenham vivas nas diversas actuações que
                o coro vai fazendo.
              </p>
              <p>
                Em 2023 estende as suas actividades a Penamacor com o projecto
                “Cura na Raia”, mais focado nas tradições musicais da Beira e no
                Adufe, promovem-se oficinas de construção deste instrumento para
                adultos e crianças e estimula-se a aprendizagem do repertório de
                canções locais, transformando-as com oficinas de escritas de
                canções para melodias já existentes, em estreita colaboração com
                o Agrupamento de Escolas Ribeiro Sanches.
              </p>
              <p>
                Em 2026 o projecto cria um projecto cultural em colaboração com
                a Junta de freguesia de Benfica para a criação de um cancioneiro
                da diversidade musical de Benfica, criando diversos coros e
                oficinas a partir do registo em contínuo da música diversa e
                multi cultural que se vai encontrando na Freguesia.
              </p>
              <p>
                Desde 2023 que o projecto colabora com investigadores académicos
                de diversas universidades Ibéricas, para desenvolver modelos de
                interação entre Inteligência Artificial e música Tradicional e é
                ainda parceiro audiovisual do Arquivo Digital do Cante, para
                além de projectos pontuais com outras associações e
                instituições.
              </p>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-3 md:gap-0 mt-8">
                <a
                  className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-250 underline"
                  href="https://vimeo.com/470587297"
                  target="_blank"
                >
                  O que é a MPAGDP?
                </a>
                <a
                  className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-250 underline"
                  href="https://vimeo.com/509468023"
                  target="_blank"
                >
                  Qual o papel da MPAGDP?
                </a>
                <a
                  className="cursor-pointer text-color-2 hover:text-color-1 transition-all duration-250 underline"
                  href="mailto:amusicaportuguesa@gmail.com"
                  target="_blank"
                >
                  amusicaportuguesa@gmail.com
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;
