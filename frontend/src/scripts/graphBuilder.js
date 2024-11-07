export class RelationGraphBuilder {
    constructor(fundName, fundHolding, info) {
        this.fundName = fundName;
        this.fundHolding = fundHolding;
        this.stockInfo = {};
        this.bondInfo = {};

        console.log(info);

        for (const i of info.stock) {
            this.stockInfo[i.code] = i;
        }
        for (const i of info.bond) {
            this.bondInfo[i.code] = i;
        }

        this.nodes = [];
        this.links = [];
        this.categories = [];

        this.addedNodes = new Set();
        this.addCategories = new Set();
        this.category2index = {};
    }

    addNodeIfNotExists (id, name, category, extra) {
        const key = `${category}-${id}`;
        if (!this.addedNodes.has(key)) {
            this.nodes.push({
                id: id,
                name: name,
                category: category,
                extra: extra
            });
            this.addedNodes.add(key);
        }
        return id;
    }

    addLink (source, target) {
        this.links.push({
            source: source,
            target: target
        })
    }

    getCategoryIndex (category) {
        if (!this.addCategories.has(category)) {
            this.addCategories.add(category);
            this.category2index[category] = this.categories.length;
            this.categories.push({ name: category });
        }
        return this.category2index[category];
    }

    build () {

        for (const [fundCode, holding] of Object.entries(this.fundHolding)) {
            const fid = this.addNodeIfNotExists(
                fundCode, this.fundName[fundCode],
                this.getCategoryIndex('基金'), {}
            );
            for (const s of holding.stock) {
                const sInfo = this.stockInfo[s.code];
                console.log(s);
                console.log(sInfo);

                const sid = this.addNodeIfNotExists(
                    s.code, s.name, this.getCategoryIndex('股票'),
                    sInfo ? { abbr: sInfo.abbreviation, code: sInfo.code, name: sInfo.name } : {}
                );
                this.addLink(fid, sid);

                if (sInfo === undefined) {
                    continue;
                }

                const iid = this.addNodeIfNotExists(
                    sInfo.industry, sInfo.industry, this.getCategoryIndex('所处行业'), {}
                );
                this.addLink(sid, iid);

                const mid = this.addNodeIfNotExists(
                    sInfo.market, sInfo.market, this.getCategoryIndex('所在市场'), {}
                );
                this.addLink(sid, mid);
            }
            for (const b of holding.bond) {
                const bInfo = this.bondInfo[b.code];
                const bid = this.addNodeIfNotExists(
                    b.code, b.name, this.getCategoryIndex('债券'),
                    bInfo ? { abbr: bInfo.abbreviation, code: bInfo.code, name: bInfo.name } : {}
                );
                this.addLink(fid, bid);

                if (bInfo === undefined) {
                    continue;
                }

                const lid = this.addNodeIfNotExists(
                    bInfo.level, bInfo.level, this.getCategoryIndex('信用评级'), {}
                );
                this.addLink(bid, lid);

                const tid = this.addNodeIfNotExists(
                    bInfo.type, bInfo.type, this.getCategoryIndex('债券类型'), {}
                );
                this.addLink(bid, tid);
            }
        }

        console.log(this.nodes);
        console.log(this.links);
        console.log(this.categories);

        return {
            nodes: this.nodes,
            links: this.links,
            categories: this.categories
        };
    }
}
